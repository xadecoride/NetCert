package http

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/usecase"
)

type QuickLabHandler struct {
	quickLabUC *usecase.QuickLabUseCase
}

func NewQuickLabHandler(quickLabUC *usecase.QuickLabUseCase) *QuickLabHandler {
	return &QuickLabHandler{quickLabUC: quickLabUC}
}

// ListQuickLabs returns all quick labs, optionally filtered by track_id.
func (h *QuickLabHandler) ListQuickLabs(w http.ResponseWriter, r *http.Request) {
	trackIDStr := r.URL.Query().Get("track_id")
	var trackID uuid.UUID
	if trackIDStr != "" {
		var err error
		trackID, err = uuid.Parse(trackIDStr)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid track_id"})
			return
		}
	}

	labs, err := h.quickLabUC.ListQuickLabs(r.Context(), trackID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch quick labs"})
		return
	}
	if labs == nil {
		labs = []domain.QuickLab{}
	}
	writeJSON(w, http.StatusOK, labs)
}

// GetQuickLab returns a single quick lab by ID.
func (h *QuickLabHandler) GetQuickLab(w http.ResponseWriter, r *http.Request) {
	labID, err := uuid.Parse(chi.URLParam(r, "labId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid quick lab id"})
		return
	}

	lab, err := h.quickLabUC.GetQuickLab(r.Context(), labID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch quick lab"})
		return
	}
	if lab == nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "quick lab not found"})
		return
	}

	writeJSON(w, http.StatusOK, lab)
}
