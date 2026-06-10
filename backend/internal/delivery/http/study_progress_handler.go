package http

import (
	"encoding/json"
	"net/http"

	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/middleware"
	"github.com/netcert/backend/internal/usecase"
)

type StudyProgressHandler struct {
	progressUseCase *usecase.StudyProgressUseCase
}

func NewStudyProgressHandler(progressUseCase *usecase.StudyProgressUseCase) *StudyProgressHandler {
	return &StudyProgressHandler{progressUseCase: progressUseCase}
}

func (h *StudyProgressHandler) GetProgress(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())

	progress, err := h.progressUseCase.GetProgress(r.Context(), userID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch study progress"})
		return
	}

	if progress == nil {
		progress = []domain.StudyProgress{}
	}

	writeJSON(w, http.StatusOK, progress)
}

func (h *StudyProgressHandler) ToggleGuide(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())

	var req domain.StudyProgressToggleRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	if err := h.progressUseCase.ToggleGuide(r.Context(), userID, req); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to toggle guide progress"})
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}
