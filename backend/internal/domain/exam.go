package domain

import (
	"time"

	"github.com/google/uuid"
)

type Vendor string

const (
	VendorJuniper Vendor = "juniper"
	VendorCisco   Vendor = "cisco"
)

type Level string

const (
	LevelJNCIA Level = "JNCIA"
	LevelJNCIP Level = "JNCIP"
	LevelJNCIE Level = "JNCIE"
	LevelCCNA  Level = "CCNA"
	LevelCCNP  Level = "CCNP"
	LevelCCIE  Level = "CCIE"
)

type Track struct {
	ID          uuid.UUID `json:"id"`
	Slug        string    `json:"slug"`
	Vendor      Vendor    `json:"vendor"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	IconURL     *string   `json:"icon_url,omitempty"`
	SortOrder   int       `json:"sort_order"`
	CreatedAt   time.Time `json:"created_at"`
}

type Exam struct {
	ID              uuid.UUID `json:"id"`
	TrackID         uuid.UUID `json:"track_id"`
	Code            string    `json:"code"`
	Name            string    `json:"name"`
	Level           Level     `json:"level"`
	DurationMinutes int       `json:"duration_minutes"`
	TotalQuestions  int       `json:"total_questions"`
	PassingScore    float64   `json:"passing_score"`
	BlueprintURL    *string   `json:"blueprint_url,omitempty"`
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
}
