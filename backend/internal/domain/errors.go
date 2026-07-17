package domain

import "errors"

// Sentinel domain errors. Used across usecase and delivery layers.
// Handlers should map these to HTTP statuses via a central mapper
// (see Phase 1.5 of ROADMAP_DEV.md) rather than leaking err.Error().

var (
	// ErrNotFound — ресурс не существует.
	ErrNotFound = errors.New("not found")

	// ErrForbidden — аутентифицированный пользователь не имеет прав на ресурс (IDOR-защита).
	ErrForbidden = errors.New("forbidden")

	// ErrConflict — нарушение уникальности/состояния.
	ErrConflict = errors.New("conflict")

	// ErrValidation — некорректный ввод (не прошёл validator.Struct).
	ErrValidation = errors.New("validation error")
)
