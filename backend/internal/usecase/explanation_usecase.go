package usecase

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

var (
	ErrExplanationNotFound = errors.New("explanation not found")
	ErrExplanationNoAccess = errors.New("you must attempt this question before viewing the explanation")
)

type ExplanationUseCase struct {
	explanationRepo domain.ExplanationRepository
	attemptRepo     domain.AttemptRepository
}

func NewExplanationUseCase(explanationRepo domain.ExplanationRepository, attemptRepo domain.AttemptRepository) *ExplanationUseCase {
	return &ExplanationUseCase{explanationRepo: explanationRepo, attemptRepo: attemptRepo}
}

// GetExplanation returns the latest explanation for a question.
// Access is granted only if the user has answered this question in an attempt.
func (uc *ExplanationUseCase) GetExplanation(ctx context.Context, questionID uuid.UUID, userID uuid.UUID) (*domain.Explanation, error) {
	// Check access: user must have answered this question
	hasAccess, err := uc.hasUserAnsweredQuestion(ctx, questionID, userID)
	if err != nil {
		return nil, err
	}
	if !hasAccess {
		return nil, ErrExplanationNoAccess
	}

	explanation, err := uc.explanationRepo.FindByQuestionID(ctx, questionID)
	if err != nil {
		return nil, ErrExplanationNotFound
	}

	return explanation, nil
}

// GetExplanationVersion returns a specific version of an explanation
func (uc *ExplanationUseCase) GetExplanationVersion(ctx context.Context, questionID uuid.UUID, version int, userID uuid.UUID) (*domain.Explanation, error) {
	hasAccess, err := uc.hasUserAnsweredQuestion(ctx, questionID, userID)
	if err != nil {
		return nil, err
	}
	if !hasAccess {
		return nil, ErrExplanationNoAccess
	}

	explanation, err := uc.explanationRepo.FindVersionByQuestionID(ctx, questionID, version)
	if err != nil {
		return nil, ErrExplanationNotFound
	}

	return explanation, nil
}

// BatchSendTelemetry saves a batch of telemetry events
func (uc *ExplanationUseCase) BatchSendTelemetry(ctx context.Context, userID uuid.UUID, req domain.BatchTelemetryRequest) error {
	if len(req.Events) == 0 {
		return nil
	}
	if len(req.Events) > 50 {
		req.Events = req.Events[:50]
	}
	return uc.explanationRepo.SaveTelemetryEvents(ctx, userID, req.Events)
}

// hasUserAnsweredQuestion checks via direct SQL if the user has answered this question
func (uc *ExplanationUseCase) hasUserAnsweredQuestion(ctx context.Context, questionID uuid.UUID, userID uuid.UUID) (bool, error) {
	return uc.attemptRepo.HasUserAnsweredQuestion(ctx, questionID, userID)
}
