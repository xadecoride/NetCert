package usecase

import (
	"context"
	"encoding/json"
	"errors"
	"time"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/pkg/hash"
	jwtpkg "github.com/netcert/backend/internal/pkg/jwt"
)

var (
	ErrUserNotFound      = errors.New("user not found")
	ErrInvalidCredentials = errors.New("invalid credentials")
	ErrEmailAlreadyExists = errors.New("email already exists")
)

type AuthUseCase struct {
	userRepo   domain.UserRepository
	jwtManager *jwtpkg.JWTManager
}

func NewAuthUseCase(userRepo domain.UserRepository, jwtManager *jwtpkg.JWTManager) *AuthUseCase {
	return &AuthUseCase{userRepo: userRepo, jwtManager: jwtManager}
}

func (uc *AuthUseCase) Register(ctx context.Context, req domain.RegisterRequest) (*domain.AuthResponse, error) {
	existing, _ := uc.userRepo.FindByEmail(ctx, req.Email)
	if existing != nil {
		return nil, ErrEmailAlreadyExists
	}

	hashedPassword, err := hash.HashPassword(req.Password)
	if err != nil {
		return nil, err
	}

	now := time.Now()
	user := &domain.User{
		ID:              uuid.New(),
		Email:           req.Email,
		PasswordHash:    hashedPassword,
		DisplayName:     req.DisplayName,
		Role:            domain.RoleStudent,
		IsEmailVerified: false,
		StreakDays:      0,
		TotalXP:         0,
		CreatedAt:       now,
		UpdatedAt:       now,
	}

	if err := uc.userRepo.Create(ctx, user); err != nil {
		return nil, err
	}

	accessToken, err := uc.jwtManager.GenerateAccessToken(user.ID, user.Email, string(user.Role))
	if err != nil {
		return nil, err
	}

	refreshToken, err := uc.jwtManager.GenerateRefreshToken(user.ID)
	if err != nil {
		return nil, err
	}

	return &domain.AuthResponse{
		User:         *user,
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresIn:    int(uc.jwtManager.AccessTokenTTL().Seconds()),
	}, nil
}

func (uc *AuthUseCase) Login(ctx context.Context, req domain.LoginRequest) (*domain.AuthResponse, error) {
	user, err := uc.userRepo.FindByEmail(ctx, req.Email)
	if err != nil {
		return nil, ErrInvalidCredentials
	}

	if !hash.CheckPassword(req.Password, user.PasswordHash) {
		return nil, ErrInvalidCredentials
	}

	accessToken, err := uc.jwtManager.GenerateAccessToken(user.ID, user.Email, string(user.Role))
	if err != nil {
		return nil, err
	}

	refreshToken, err := uc.jwtManager.GenerateRefreshToken(user.ID)
	if err != nil {
		return nil, err
	}

	return &domain.AuthResponse{
		User:         *user,
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresIn:    int(uc.jwtManager.AccessTokenTTL().Seconds()),
	}, nil
}

func (uc *AuthUseCase) DevLogin(ctx context.Context, email string) (*domain.AuthResponse, error) {
	// Try to find existing user
	user, err := uc.userRepo.FindByEmail(ctx, email)
	if err != nil {
		// Create new dev user
		now := time.Now()
		user = &domain.User{
			ID:              uuid.New(),
			Email:           email,
			PasswordHash:    "",
			DisplayName:     "Dev User",
			Role:            domain.RoleStudent,
			IsEmailVerified: true,
			StreakDays:      0,
			TotalXP:         0,
			CreatedAt:       now,
			UpdatedAt:       now,
		}
		if err := uc.userRepo.Create(ctx, user); err != nil {
			return nil, err
		}
	}

	accessToken, err := uc.jwtManager.GenerateAccessToken(user.ID, user.Email, string(user.Role))
	if err != nil {
		return nil, err
	}

	refreshToken, err := uc.jwtManager.GenerateRefreshToken(user.ID)
	if err != nil {
		return nil, err
	}

	return &domain.AuthResponse{
		User:         *user,
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresIn:    int(uc.jwtManager.AccessTokenTTL().Seconds()),
	}, nil
}

func (uc *AuthUseCase) GetProfile(ctx context.Context, userID uuid.UUID) (*domain.User, error) {
	user, err := uc.userRepo.FindByID(ctx, userID)
	if err != nil {
		return nil, ErrUserNotFound
	}
	return user, nil
}

type UpdateProfileRequest struct {
	DisplayName string  `json:"display_name,omitempty"`
	AvatarURL   *string `json:"avatar_url,omitempty"`
}

func (uc *AuthUseCase) UpdateProfile(ctx context.Context, userID uuid.UUID, req UpdateProfileRequest) (*domain.User, error) {
	user, err := uc.userRepo.FindByID(ctx, userID)
	if err != nil {
		return nil, ErrUserNotFound
	}

	if req.DisplayName != "" {
		user.DisplayName = req.DisplayName
	}
	if req.AvatarURL != nil {
		user.AvatarURL = req.AvatarURL
	}

	if err := uc.userRepo.Update(ctx, user); err != nil {
		return nil, err
	}
	return user, nil
}

func (uc *AuthUseCase) UpdatePreferences(ctx context.Context, userID uuid.UUID, prefs json.RawMessage) (*domain.User, error) {
	if err := uc.userRepo.UpdatePreferences(ctx, userID, prefs); err != nil {
		return nil, err
	}
	return uc.userRepo.FindByID(ctx, userID)
}

func (uc *AuthUseCase) UpdateEmail(ctx context.Context, userID uuid.UUID, email string) error {
	user, err := uc.userRepo.FindByID(ctx, userID)
	if err != nil {
		return ErrUserNotFound
	}

	// Check if email already taken
	existing, _ := uc.userRepo.FindByEmail(ctx, email)
	if existing != nil && existing.ID != userID {
		return ErrEmailAlreadyExists
	}

	user.Email = email
	user.IsEmailVerified = false
	return uc.userRepo.Update(ctx, user)
}
