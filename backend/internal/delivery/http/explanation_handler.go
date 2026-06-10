package http

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/middleware"
	"github.com/netcert/backend/internal/usecase"
)

type ExplanationHandler struct {
	explanationUseCase *usecase.ExplanationUseCase
}

func NewExplanationHandler(explanationUseCase *usecase.ExplanationUseCase) *ExplanationHandler {
	return &ExplanationHandler{explanationUseCase: explanationUseCase}
}

// GetExplanation returns the deep-dive explanation for a question
func (h *ExplanationHandler) GetExplanation(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	questionID, err := uuid.Parse(chi.URLParam(r, "questionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid question id"})
		return
	}

	explanation, err := h.explanationUseCase.GetExplanation(r.Context(), questionID, userID)
	if err != nil {
		if errors.Is(err, usecase.ErrExplanationNotFound) {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "explanation not found"})
			return
		}
		if errors.Is(err, usecase.ErrExplanationNoAccess) {
			writeJSON(w, http.StatusForbidden, map[string]string{"error": "you must answer this question first"})
			return
		}
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch explanation"})
		return
	}

	writeJSON(w, http.StatusOK, explanation)
}

// GetExplanationVersion returns a specific version of an explanation
func (h *ExplanationHandler) GetExplanationVersion(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	questionID, err := uuid.Parse(chi.URLParam(r, "questionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid question id"})
		return
	}

	versionStr := r.URL.Query().Get("version")
	if versionStr == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "version query parameter required"})
		return
	}

	version, err := strconv.Atoi(versionStr)
	if err != nil || version < 1 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "version must be a positive integer"})
		return
	}

	explanation, err := h.explanationUseCase.GetExplanationVersion(r.Context(), questionID, version, userID)
	if err != nil {
		if errors.Is(err, usecase.ErrExplanationNotFound) {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "explanation version not found"})
			return
		}
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch explanation"})
		return
	}

	writeJSON(w, http.StatusOK, explanation)
}

// BatchSendTelemetry accepts a batch of explanation telemetry events
func (h *ExplanationHandler) BatchSendTelemetry(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())

	var req domain.BatchTelemetryRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	if err := h.explanationUseCase.BatchSendTelemetry(r.Context(), userID, req); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to save telemetry"})
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}
