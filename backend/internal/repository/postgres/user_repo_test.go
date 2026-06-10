package postgres

import (
	"context"
	"encoding/json"
	"errors"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/netcert/backend/internal/domain"
)

func TestUserRepository_Create(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()

	user := &domain.User{
		ID:              uuid.New(),
		Email:           "test@example.com",
		PasswordHash:    "hashed_password",
		DisplayName:     "Test User",
		Role:            domain.RoleStudent,
		IsEmailVerified: false,
		StreakDays:      0,
		TotalXP:         0,
		CreatedAt:       time.Now(),
		UpdatedAt:       time.Now(),
	}

	pool.ExpectExec(`INSERT INTO users`).
		WithArgs(user.ID, user.Email, user.PasswordHash, user.DisplayName, user.Role,
			user.IsEmailVerified, user.StreakDays, user.TotalXP, user.CreatedAt, user.UpdatedAt).
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	err = repo.Create(ctx, user)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestUserRepository_Create_Error(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()

	user := &domain.User{ID: uuid.New(), Email: "test@example.com"}
	pool.ExpectExec(`INSERT INTO users`).
		WithArgs(user.ID, user.Email, user.PasswordHash, user.DisplayName, user.Role,
			user.IsEmailVerified, user.StreakDays, user.TotalXP, user.CreatedAt, user.UpdatedAt).
		WillReturnError(errors.New("duplicate key"))

	err = repo.Create(ctx, user)
	assert.Error(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestUserRepository_FindByEmail(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()
	email := "test@example.com"
	id := uuid.New()

	rows := pgxmock.NewRows([]string{
		"id", "email", "password_hash", "display_name", "role", "avatar_url",
		"oauth_provider", "oauth_id", "is_email_verified", "streak_days",
		"total_xp", "preferences", "created_at", "updated_at",
	}).AddRow(id, email, "hash", "Test", "student", nil, nil, nil, true, 3, 100, nil, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM users WHERE email`).WithArgs(email).WillReturnRows(rows)

	user, err := repo.FindByEmail(ctx, email)
	require.NoError(t, err)
	assert.Equal(t, id, user.ID)
	assert.Equal(t, email, user.Email)
	assert.Equal(t, "Test", user.DisplayName)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestUserRepository_FindByEmail_NotFound(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()

	pool.ExpectQuery(`SELECT .+ FROM users WHERE email`).
		WithArgs("nonexistent@example.com").
		WillReturnError(pgx.ErrNoRows)

	user, err := repo.FindByEmail(ctx, "nonexistent@example.com")
	assert.Error(t, err)
	assert.Nil(t, user)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestUserRepository_FindByID(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()
	id := uuid.New()

	rows := pgxmock.NewRows([]string{
		"id", "email", "password_hash", "display_name", "role", "avatar_url",
		"oauth_provider", "oauth_id", "is_email_verified", "streak_days",
		"total_xp", "preferences", "created_at", "updated_at",
	}).AddRow(id, "test@example.com", "hash", "Test User", "student", nil, nil, nil, true, 5, 200, nil, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM users WHERE id`).WithArgs(id).WillReturnRows(rows)

	user, err := repo.FindByID(ctx, id)
	require.NoError(t, err)
	assert.Equal(t, id, user.ID)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestUserRepository_Update(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()

	user := &domain.User{
		ID:            uuid.New(),
		DisplayName:   "Updated Name",
		UpdatedAt:     time.Now(),
	}

	pool.ExpectExec(`UPDATE users SET`).
		WithArgs(user.DisplayName, user.AvatarURL, user.StreakDays, user.TotalXP,
			user.IsEmailVerified, user.Preferences, pgxmock.AnyArg(), user.ID).
		WillReturnResult(pgxmock.NewResult("UPDATE", 1))

	err = repo.Update(ctx, user)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestUserRepository_UpdatePreferences(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewUserRepository(pool)
	ctx := context.Background()
	userID := uuid.New()
	prefs := json.RawMessage(`{"language":"en"}`)

	pool.ExpectExec(`UPDATE users SET preferences`).
		WithArgs(prefs, pgxmock.AnyArg(), userID).
		WillReturnResult(pgxmock.NewResult("UPDATE", 1))

	err = repo.UpdatePreferences(ctx, userID, prefs)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}
