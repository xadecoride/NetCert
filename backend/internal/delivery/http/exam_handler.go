package http

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/middleware"
	"github.com/netcert/backend/internal/usecase"
)

type ExamHandler struct {
	examUseCase *usecase.ExamUseCase
}

func NewExamHandler(examUseCase *usecase.ExamUseCase) *ExamHandler {
	return &ExamHandler{examUseCase: examUseCase}
}

func (h *ExamHandler) ListTracks(w http.ResponseWriter, r *http.Request) {
	tracks, err := h.examUseCase.ListTracks(r.Context())
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch tracks"})
		return
	}
	if tracks == nil {
		tracks = []domain.Track{}
	}
	writeJSON(w, http.StatusOK, tracks)
}

func (h *ExamHandler) GetTrack(w http.ResponseWriter, r *http.Request) {
	slug := chi.URLParam(r, "slug")
	track, err := h.examUseCase.GetTrack(r.Context(), slug)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "track not found"})
		return
	}
	writeJSON(w, http.StatusOK, track)
}

func (h *ExamHandler) ListExams(w http.ResponseWriter, r *http.Request) {
	slug := chi.URLParam(r, "slug")
	track, err := h.examUseCase.GetTrack(r.Context(), slug)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "track not found"})
		return
	}
	exams, err := h.examUseCase.ListExams(r.Context(), track.ID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch exams"})
		return
	}
	if exams == nil {
		exams = []domain.Exam{}
	}
	writeJSON(w, http.StatusOK, exams)
}

func (h *ExamHandler) GetExam(w http.ResponseWriter, r *http.Request) {
	examID, err := uuid.Parse(chi.URLParam(r, "examId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid exam id"})
		return
	}
	exam, err := h.examUseCase.GetExam(r.Context(), examID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "exam not found"})
		return
	}
	writeJSON(w, http.StatusOK, exam)
}

func (h *ExamHandler) GetExamQuestions(w http.ResponseWriter, r *http.Request) {
	examID, err := uuid.Parse(chi.URLParam(r, "examId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid exam id"})
		return
	}
	lang := r.URL.Query().Get("lang")
	questions, err := h.examUseCase.GetExamQuestions(r.Context(), examID, lang)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch questions"})
		return
	}
	if questions == nil {
		questions = []domain.Question{}
	}
	writeJSON(w, http.StatusOK, questions)
}

func (h *ExamHandler) StartAttempt(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())

	var req domain.StartAttemptRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	attempt, err := h.examUseCase.StartAttempt(r.Context(), userID, req)
	if err != nil {
		if err == usecase.ErrExamNotFound {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "exam not found"})
			return
		}
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to start attempt"})
		return
	}

	writeJSON(w, http.StatusCreated, attempt)
}

func (h *ExamHandler) GetAttempt(w http.ResponseWriter, r *http.Request) {
	attemptID, err := uuid.Parse(chi.URLParam(r, "attemptId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid attempt id"})
		return
	}

	attempt, err := h.examUseCase.GetAttempt(r.Context(), attemptID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "attempt not found"})
		return
	}

	writeJSON(w, http.StatusOK, attempt)
}

func (h *ExamHandler) SubmitAnswer(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	attemptID, err := uuid.Parse(chi.URLParam(r, "attemptId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid attempt id"})
		return
	}

	var req domain.SubmitAnswerRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	answer, err := h.examUseCase.SubmitAnswer(r.Context(), attemptID, userID, req)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, answer)
}

func (h *ExamHandler) CompleteAttempt(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	attemptID, err := uuid.Parse(chi.URLParam(r, "attemptId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid attempt id"})
		return
	}

	attempt, err := h.examUseCase.CompleteAttempt(r.Context(), attemptID, userID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, attempt)
}

func (h *ExamHandler) GetAttemptWithDetails(w http.ResponseWriter, r *http.Request) {
	attemptID, err := uuid.Parse(chi.URLParam(r, "attemptId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid attempt id"})
		return
	}

	details, err := h.examUseCase.GetAttemptWithDetails(r.Context(), attemptID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "attempt not found"})
		return
	}

	writeJSON(w, http.StatusOK, details)
}

func (h *ExamHandler) GetAttemptQuestions(w http.ResponseWriter, r *http.Request) {
	attemptID, err := uuid.Parse(chi.URLParam(r, "attemptId"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid attempt id"})
		return
	}

	questions, err := h.examUseCase.GetAttemptQuestions(r.Context(), attemptID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "attempt not found"})
		return
	}

	if questions == nil {
		questions = []domain.Question{}
	}
	writeJSON(w, http.StatusOK, questions)
}

func (h *ExamHandler) GetHistory(w http.ResponseWriter, r *http.Request) {
	userID := middleware.GetUserID(r.Context())
	attempts, err := h.examUseCase.GetAttemptHistory(r.Context(), userID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "failed to fetch history"})
		return
	}
	if attempts == nil {
		attempts = []domain.Attempt{}
	}
	writeJSON(w, http.StatusOK, attempts)
}
