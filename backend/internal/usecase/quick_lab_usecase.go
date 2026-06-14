package usecase

import (
	"context"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

// QuickLabRepository defines the storage interface for quick labs.
type QuickLabRepository interface {
	GetByID(ctx context.Context, id uuid.UUID) (*domain.QuickLab, error)
	GetBySlug(ctx context.Context, slug string) (*domain.QuickLab, error)
	ListByTrack(ctx context.Context, trackID uuid.UUID) ([]domain.QuickLab, error)
	ListAll(ctx context.Context) ([]domain.QuickLab, error)
}

// QuickLabUseCase handles business logic for quick labs.
type QuickLabUseCase struct {
	repo QuickLabRepository
}

// NewQuickLabUseCase creates a new QuickLabUseCase.
func NewQuickLabUseCase(repo QuickLabRepository) *QuickLabUseCase {
	return &QuickLabUseCase{repo: repo}
}

// GetQuickLab returns a single quick lab by ID.
func (uc *QuickLabUseCase) GetQuickLab(ctx context.Context, id uuid.UUID) (*domain.QuickLab, error) {
	return uc.repo.GetByID(ctx, id)
}

// GetQuickLabBySlug returns a single quick lab by slug.
func (uc *QuickLabUseCase) GetQuickLabBySlug(ctx context.Context, slug string) (*domain.QuickLab, error) {
	return uc.repo.GetBySlug(ctx, slug)
}

// ListQuickLabs returns quick labs filtered by track.
func (uc *QuickLabUseCase) ListQuickLabs(ctx context.Context, trackID uuid.UUID) ([]domain.QuickLab, error) {
	if trackID == uuid.Nil {
		return uc.repo.ListAll(ctx)
	}
	return uc.repo.ListByTrack(ctx, trackID)
}
