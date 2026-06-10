package domain

import (
	"time"

	"github.com/google/uuid"
)

type StudyProgress struct {
	ID          uuid.UUID `json:"id"`
	UserID      uuid.UUID `json:"user_id"`
	GuideID     string    `json:"guide_id"`
	CompletedAt time.Time `json:"completed_at"`
	CreatedAt   time.Time `json:"created_at"`
}

type StudyProgressToggleRequest struct {
	GuideID    string `json:"guide_id" validate:"required"`
	Completed bool   `json:"completed"`
}
