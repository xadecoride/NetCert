package domain

import (
	"encoding/json"
	"time"

	"github.com/google/uuid"
)

type Role string

const (
	RoleStudent   Role = "student"
	RoleInstructor Role = "instructor"
	RoleAdmin     Role = "admin"
)

type User struct {
	ID                uuid.UUID       `json:"id"`
	Email             string          `json:"email"`
	PasswordHash      string          `json:"-"`
	DisplayName       string          `json:"display_name"`
	Role              Role            `json:"role"`
	AvatarURL         *string         `json:"avatar_url,omitempty"`
	OAuthProvider     *string         `json:"oauth_provider,omitempty"`
	OAuthID           *string         `json:"oauth_id,omitempty"`
	IsEmailVerified   bool            `json:"is_email_verified"`
	StreakDays        int             `json:"streak_days"`
	TotalXP           int64           `json:"total_xp"`
	Preferences       json.RawMessage `json:"preferences,omitempty"`
	CreatedAt         time.Time       `json:"created_at"`
	UpdatedAt         time.Time       `json:"updated_at"`
}

type RegisterRequest struct {
	Email       string `json:"email" validate:"required,email"`
	Password    string `json:"password" validate:"required,min=8"`
	DisplayName string `json:"display_name" validate:"required,min=2,max=100"`
}

type LoginRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

type AuthResponse struct {
	User         User   `json:"user"`
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
	ExpiresIn    int    `json:"expires_in"`
}

type TokenPair struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
	ExpiresIn    int    `json:"expires_in"`
}
