package http

import (
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"

	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/repository/postgres"
	"github.com/netcert/backend/internal/usecase"
	jwtpkg "github.com/netcert/backend/internal/pkg/jwt"
)

// testJWTManager creates a JWT manager for use in tests
func testJWTManager() *jwtpkg.JWTManager {
	return jwtpkg.NewJWTManager("test-secret-for-handler-tests", 900, 604800)
}

// testAuthToken generates a valid JWT token for a user for use in test requests
func testAuthToken(jwtMgr *jwtpkg.JWTManager, userID uuid.UUID) string {
	token, err := jwtMgr.GenerateAccessToken(userID, "test@example.com", "student")
	if err != nil {
		panic(err)
	}
	return token
}

func TestAuthHandler_Register_Success(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	jwtMgr := testJWTManager()

	// FindByEmail returns not found (email available)
	pool.ExpectQuery(`SELECT .+ FROM users WHERE email`).
		WithArgs("new@example.com").
		WillReturnError(errors.New("not found"))

	// Create user succeeds
	pool.ExpectExec(`INSERT INTO users`).
		WithArgs(pgxmock.AnyArg(), "new@example.com", pgxmock.AnyArg(), "Test User",
			domain.RoleStudent, false, 0, int64(0), pgxmock.AnyArg(), pgxmock.AnyArg()).
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	userRepo := postgres.NewUserRepository(pool)
	authUC := usecase.NewAuthUseCase(userRepo, jwtMgr)
	handler := NewAuthHandler(authUC)

	body := `{"email":"new@example.com","password":"password123","display_name":"Test User"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/register", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Register(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	var resp domain.AuthResponse
	err = json.NewDecoder(w.Body).Decode(&resp)
	require.NoError(t, err)
	assert.NotEmpty(t, resp.AccessToken)
	assert.Equal(t, "new@example.com", resp.User.Email)
	assert.Equal(t, "Test User", resp.User.DisplayName)
}

func TestAuthHandler_Register_EmailConflict(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	jwtMgr := testJWTManager()

	// FindByEmail returns existing user
	id := uuid.New()
	rows := pgxmock.NewRows([]string{
		"id", "email", "password_hash", "display_name", "role", "avatar_url",
		"oauth_provider", "oauth_id", "is_email_verified", "streak_days",
		"total_xp", "preferences", "created_at", "updated_at",
	}).AddRow(id, "taken@example.com", "hash", "Existing", "student", nil, nil, nil, true, 0, 0, nil, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM users WHERE email`).
		WithArgs("taken@example.com").
		WillReturnRows(rows)

	userRepo := postgres.NewUserRepository(pool)
	authUC := usecase.NewAuthUseCase(userRepo, jwtMgr)
	handler := NewAuthHandler(authUC)

	body := `{"email":"taken@example.com","password":"password123","display_name":"Someone"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/register", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Register(w, req)

	assert.Equal(t, http.StatusConflict, w.Code)
}

func TestAuthHandler_Login_Success(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	jwtMgr := testJWTManager()

	// Hash a password using bcrypt for the test
	pwdHash := hashPasswordForHandlerTest("password123")

	id := uuid.New()
	rows := pgxmock.NewRows([]string{
		"id", "email", "password_hash", "display_name", "role", "avatar_url",
		"oauth_provider", "oauth_id", "is_email_verified", "streak_days",
		"total_xp", "preferences", "created_at", "updated_at",
	}).AddRow(id, "user@example.com", pwdHash, "Test User", "student", nil, nil, nil, true, 0, 0, nil, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM users WHERE email`).
		WithArgs("user@example.com").
		WillReturnRows(rows)

	userRepo := postgres.NewUserRepository(pool)
	authUC := usecase.NewAuthUseCase(userRepo, jwtMgr)
	handler := NewAuthHandler(authUC)

	body := `{"email":"user@example.com","password":"password123"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Login(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var resp domain.AuthResponse
	err = json.NewDecoder(w.Body).Decode(&resp)
	require.NoError(t, err)
	assert.NotEmpty(t, resp.AccessToken)
	assert.Equal(t, "user@example.com", resp.User.Email)
}

func TestAuthHandler_Login_InvalidCredentials(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	jwtMgr := testJWTManager()

	// User not found
	pool.ExpectQuery(`SELECT .+ FROM users WHERE email`).
		WithArgs("wrong@example.com").
		WillReturnError(errors.New("not found"))

	userRepo := postgres.NewUserRepository(pool)
	authUC := usecase.NewAuthUseCase(userRepo, jwtMgr)
	handler := NewAuthHandler(authUC)

	body := `{"email":"wrong@example.com","password":"wrong"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Login(w, req)

	assert.Equal(t, http.StatusUnauthorized, w.Code)
}

// hashPasswordForHandlerTest hashes a password for handler tests using bcrypt
func hashPasswordForHandlerTest(password string) string {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.MinCost)
	if err != nil {
		panic(err)
	}
	return string(bytes)
}
