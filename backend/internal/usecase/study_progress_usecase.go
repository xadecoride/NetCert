package usecase

import (
	"context"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

type StudyProgressUseCase struct {
	progressRepo domain.StudyProgressRepository
}

func NewStudyProgressUseCase(progressRepo domain.StudyProgressRepository) *StudyProgressUseCase {
	return &StudyProgressUseCase{progressRepo: progressRepo}
}

func (uc *StudyProgressUseCase) GetProgress(ctx context.Context, userID uuid.UUID) ([]domain.StudyProgress, error) {
	return uc.progressRepo.ListByUser(ctx, userID)
}

func (uc *StudyProgressUseCase) ToggleGuide(ctx context.Context, userID uuid.UUID, req domain.StudyProgressToggleRequest) error {
	return uc.progressRepo.Upsert(ctx, userID, req.GuideID, req.Completed)
}
