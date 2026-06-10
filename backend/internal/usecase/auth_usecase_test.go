package usecase

import (
	"context"
	"encoding/json"
	"errors"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	jwtpkg "github.com/netcert/backend/internal/pkg/jwt"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// mockUserRepository is a test double for domain.UserRepository.
type mockUserRepository struct {
	users       map[string]*domain.User
	createErr   error
	findByEmail func(email string) (*domain.User, error)
}

func newMockUserRepository() *mockUserRepository {
	return &mockUserRepository{
		users: make(map[string]*domain.User),
	}
}

func (m *mockUserRepository) Create(ctx context.Context, user *domain.User) error {
	if m.createErr != nil {
		return m.createErr
	}
	m.users[user.Email] = user
	return nil
}

func (m *mockUserRepository) FindByID(ctx context.Context, id uuid.UUID) (*domain.User, error) {
	for _, u := range m.users {
		if u.ID == id {
			return u, nil
		}
	}
	return nil, errors.New("user not found")
}

func (m *mockUserRepository) FindByEmail(ctx context.Context, email string) (*domain.User, error) {
	if m.findByEmail != nil {
		return m.findByEmail(email)
	}
	if u, ok := m.users[email]; ok {
		return u, nil
	}
	return nil, errors.New("user not found")
}

func (m *mockUserRepository) Update(ctx context.Context, user *domain.User) error {
	m.users[user.Email] = user
	return nil
}

func (m *mockUserRepository) UpdatePreferences(ctx context.Context, userID uuid.UUID, prefs json.RawMessage) error {
	return nil
}

func TestAuthUseCase_Register(t *testing.T) {
	jwtManager := jwtpkg.NewJWTManager("test-secret-key-for-unit-tests-only", 15*time.Minute, 7*24*time.Hour)
	mockRepo := newMockUserRepository()
	uc := NewAuthUseCase(mockRepo, jwtManager)

	ctx := context.Background()
	req := domain.RegisterRequest{
		Email:       "test@example.com",
		Password:    "securePassword123",
		DisplayName: "Test User",
	}

	resp, err := uc.Register(ctx, req)
	require.NoError(t, err)
	assert.Equal(t, req.Email, resp.User.Email)
	assert.Equal(t, req.DisplayName, resp.User.DisplayName)
	assert.NotEmpty(t, resp.AccessToken)
	assert.NotEmpty(t, resp.RefreshToken)
	assert.Greater(t, resp.ExpiresIn, 0)

	// Duplicate registration should fail
	_, err = uc.Register(ctx, req)
	assert.ErrorIs(t, err, ErrEmailAlreadyExists)
}

func TestAuthUseCase_Login(t *testing.T) {
	jwtManager := jwtpkg.NewJWTManager("test-secret-key-for-unit-tests-only", 15*time.Minute, 7*24*time.Hour)
	mockRepo := newMockUserRepository()
	uc := NewAuthUseCase(mockRepo, jwtManager)

	ctx := context.Background()
	email := "login@example.com"
	password := "myPassword"

	// Register first
	_, err := uc.Register(ctx, domain.RegisterRequest{
		Email:       email,
		Password:    password,
		DisplayName: "Login User",
	})
	require.NoError(t, err)

	// Valid login
	resp, err := uc.Login(ctx, domain.LoginRequest{
		Email:    email,
		Password: password,
	})
	require.NoError(t, err)
	assert.NotEmpty(t, resp.AccessToken)

	// Wrong password
	_, err = uc.Login(ctx, domain.LoginRequest{
		Email:    email,
		Password: "wrong",
	})
	assert.ErrorIs(t, err, ErrInvalidCredentials)

	// Non-existent user
	_, err = uc.Login(ctx, domain.LoginRequest{
		Email:    "nobody@example.com",
		Password: password,
	})
	assert.ErrorIs(t, err, ErrInvalidCredentials)
}

func TestAuthUseCase_GetProfile(t *testing.T) {
	jwtManager := jwtpkg.NewJWTManager("test-secret-key-for-unit-tests-only", 15*time.Minute, 7*24*time.Hour)
	mockRepo := newMockUserRepository()
	uc := NewAuthUseCase(mockRepo, jwtManager)

	ctx := context.Background()
	registered, err := uc.Register(ctx, domain.RegisterRequest{
		Email:       "profile@example.com",
		Password:    "password",
		DisplayName: "Profile User",
	})
	require.NoError(t, err)

	user, err := uc.GetProfile(ctx, registered.User.ID)
	require.NoError(t, err)
	assert.Equal(t, registered.User.ID, user.ID)

	_, err = uc.GetProfile(ctx, uuid.New())
	assert.ErrorIs(t, err, ErrUserNotFound)
}
