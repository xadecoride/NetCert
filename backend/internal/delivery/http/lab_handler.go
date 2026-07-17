package http

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/middleware"
	"github.com/netcert/backend/internal/usecase"
)

type LabHandler struct {
	labUC *usecase.LabUseCase
}

func NewLabHandler(labUC *usecase.LabUseCase) *LabHandler {
	return &LabHandler{labUC: labUC}
}

// ListLabs returns all labs for a track (query param: ?track_id=uuid).
func (h *LabHandler) ListLabs(w http.ResponseWriter, r *http.Request) {
	trackIDStr := r.URL.Query().Get("track_id")
	if trackIDStr == "" {
		// Return all labs (without track filter)
		// For now, return empty array — real listing requires a list method
		writeJSON(w, http.StatusOK, []domain.Lab{})
		return
	}
	trackID, err := uuid.Parse(trackIDStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid track_id"})
		return
	}

	labs, err := h.labUC.ListLabs(r.Context(), trackID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch labs"})
		return
	}
	if labs == nil {
		labs = []domain.Lab{}
	}
	writeJSON(w, http.StatusOK, labs)
}

// GetLab returns a single lab by ID.
func (h *LabHandler) GetLab(w http.ResponseWriter, r *http.Request) {
	labID, err := uuid.Parse(chi.URLParam(r, "labId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid lab id"})
		return
	}

	lab, err := h.labUC.GetLab(r.Context(), labID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch lab"})
		return
	}
	if lab == nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "lab not found"})
		return
	}

	writeJSON(w, http.StatusOK, lab)
}

// StartLab starts a lab session.
func (h *LabHandler) StartLab(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	var req domain.LabStartRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	if req.LabID == uuid.Nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "lab_id is required"})
		return
	}
	if req.Mode == "" {
		req.Mode = "practice"
	}

	submission, err := h.labUC.StartLab(r.Context(), userID, &req)
	if err != nil {
		writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusCreated, submission)
}

// GetSubmission returns the status of a lab submission.
// Ownership-checked in usecase (IDOR protection — AUDIT_TECHNICAL.md §1.1).
func (h *LabHandler) GetSubmission(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	submissionID, err := uuid.Parse(chi.URLParam(r, "submissionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid submission id"})
		return
	}

	submission, err := h.labUC.GetSubmission(r.Context(), userID, submissionID)
	if err != nil {
		switch {
		case errors.Is(err, domain.ErrForbidden):
			writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		case errors.Is(err, domain.ErrNotFound):
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "submission not found"})
		default:
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch submission"})
		}
		return
	}

	writeJSON(w, http.StatusOK, submission)
}

// StopLab stops and cleans up a lab session.
func (h *LabHandler) StopLab(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	submissionID, err := uuid.Parse(chi.URLParam(r, "submissionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid submission id"})
		return
	}

	if err := h.labUC.StopLab(r.Context(), userID, submissionID); err != nil {
		writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "completed"})
}

// PauseLab pauses a lab session.
func (h *LabHandler) PauseLab(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	submissionID, err := uuid.Parse(chi.URLParam(r, "submissionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid submission id"})
		return
	}

	if err := h.labUC.PauseLab(r.Context(), userID, submissionID); err != nil {
		writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "paused"})
}

// ResumeLab resumes a paused lab session.
func (h *LabHandler) ResumeLab(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	submissionID, err := uuid.Parse(chi.URLParam(r, "submissionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid submission id"})
		return
	}

	if err := h.labUC.ResumeLab(r.Context(), userID, submissionID); err != nil {
		writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{"status": "running"})
}

// SubmitModule submits a module for grading.
func (h *LabHandler) SubmitModule(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	var req domain.LabSubmitModuleRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	score, err := h.labUC.SubmitModule(r.Context(), userID, &req)
	if err != nil {
		writeJSON(w, http.StatusConflict, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, score)
}

// GetScores returns all scores for a submission.
// Ownership-checked in usecase (IDOR protection — AUDIT_TECHNICAL.md §1.1).
func (h *LabHandler) GetScores(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	submissionID, err := uuid.Parse(chi.URLParam(r, "submissionId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid submission id"})
		return
	}

	scores, err := h.labUC.GetScores(r.Context(), userID, submissionID)
	if err != nil {
		switch {
		case errors.Is(err, domain.ErrForbidden):
			writeJSON(w, http.StatusForbidden, map[string]string{"error": "forbidden"})
		case errors.Is(err, domain.ErrNotFound):
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "submission not found"})
		default:
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch scores"})
		}
		return
	}

	writeJSON(w, http.StatusOK, scores)
}

// GetActiveSubmissions returns active lab submissions for the current user.
func (h *LabHandler) GetActiveSubmissions(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	if userID == uuid.Nil {
		writeJSON(w, http.StatusUnauthorized, map[string]string{"error": "unauthorized"})
		return
	}

	submissions, err := h.labUC.GetActiveSubmissions(r.Context(), userID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch submissions"})
		return
	}

	writeJSON(w, http.StatusOK, submissions)
}
