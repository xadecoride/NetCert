package postgres

import (
	"context"
	"encoding/json"
	"time"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

type UserRepository struct {
	pool DBPool
}

func NewUserRepository(pool DBPool) *UserRepository {
	return &UserRepository{pool: pool}
}

func (r *UserRepository) Create(ctx context.Context, user *domain.User) error {
	query := `
		INSERT INTO users (id, email, password_hash, display_name, role, is_email_verified, streak_days, total_xp, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
	`
	_, err := r.pool.Exec(ctx, query,
		user.ID, user.Email, user.PasswordHash, user.DisplayName, user.Role,
		user.IsEmailVerified, user.StreakDays, user.TotalXP, user.CreatedAt, user.UpdatedAt,
	)
	return err
}

func (r *UserRepository) FindByID(ctx context.Context, id uuid.UUID) (*domain.User, error) {
	query := `SELECT id, email, password_hash, display_name, role, avatar_url, oauth_provider, oauth_id,
		is_email_verified, streak_days, total_xp, preferences, created_at, updated_at
		FROM users WHERE id = $1`
	
	u := &domain.User{}
	err := r.pool.QueryRow(ctx, query, id).Scan(
		&u.ID, &u.Email, &u.PasswordHash, &u.DisplayName, &u.Role,
		&u.AvatarURL, &u.OAuthProvider, &u.OAuthID,
		&u.IsEmailVerified, &u.StreakDays, &u.TotalXP, &u.Preferences, &u.CreatedAt, &u.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	return u, nil
}

func (r *UserRepository) FindByEmail(ctx context.Context, email string) (*domain.User, error) {
	query := `SELECT id, email, password_hash, display_name, role, avatar_url, oauth_provider, oauth_id,
		is_email_verified, streak_days, total_xp, preferences, created_at, updated_at
		FROM users WHERE email = $1`
	
	u := &domain.User{}
	err := r.pool.QueryRow(ctx, query, email).Scan(
		&u.ID, &u.Email, &u.PasswordHash, &u.DisplayName, &u.Role,
		&u.AvatarURL, &u.OAuthProvider, &u.OAuthID,
		&u.IsEmailVerified, &u.StreakDays, &u.TotalXP, &u.Preferences, &u.CreatedAt, &u.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	return u, nil
}

func (r *UserRepository) Update(ctx context.Context, user *domain.User) error {
	query := `UPDATE users SET display_name=$1, avatar_url=$2, streak_days=$3, total_xp=$4,
		is_email_verified=$5, preferences=$6, updated_at=$7 WHERE id=$8`
	_, err := r.pool.Exec(ctx, query,
		user.DisplayName, user.AvatarURL, user.StreakDays, user.TotalXP,
		user.IsEmailVerified, user.Preferences, time.Now(), user.ID,
	)
	return err
}

func (r *UserRepository) UpdatePreferences(ctx context.Context, userID uuid.UUID, prefs json.RawMessage) error {
	query := `UPDATE users SET preferences=$1, updated_at=$2 WHERE id=$3`
	_, err := r.pool.Exec(ctx, query, prefs, time.Now(), userID)
	return err
}
