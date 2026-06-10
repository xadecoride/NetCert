package http

import (
	"net/http"
	"os"
	"strings"

	"github.com/go-chi/chi/v5"
	chimw "github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
	"github.com/netcert/backend/internal/delivery/ws"
	"github.com/netcert/backend/internal/middleware"
	"github.com/netcert/backend/internal/usecase"
	jwtpkg "github.com/netcert/backend/internal/pkg/jwt"
)

func NewRouter(
	authUC *usecase.AuthUseCase,
	examUC *usecase.ExamUseCase,
	explanationUC *usecase.ExplanationUseCase,
	labUC *usecase.LabUseCase,
	studyProgressUC *usecase.StudyProgressUseCase,
	jwtManager *jwtpkg.JWTManager,
	appEnv string,
) http.Handler {
	r := chi.NewRouter()

	// Build CORS allowed origins from env var (comma-separated), fall back to dev defaults
	allowedOrigins := parseCORSOrigins(os.Getenv("CORS_ORIGINS"))

	// Configure WebSocket upgrader with the same origin restrictions
	ws.SetAllowedOrigins(allowedOrigins)

	// Global middleware
	r.Use(chimw.Logger)
	r.Use(chimw.Recoverer)
	r.Use(chimw.RequestID)
	r.Use(chimw.RealIP)
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   allowedOrigins,
		AllowedMethods:   []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-Request-ID"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300,
	}))

	authMw := middleware.NewAuthMiddleware(jwtManager)

	// Health check
	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status":"ok","version":"1.0.0"}`))
	})

	// Lab WebSocket endpoints (public for now; will add auth later)
	sandboxHandler := ws.NewSandboxHandler(nil)
	if labUC != nil {
		sshProxy := ws.NewSSHProxy(labUC)
		r.Route("/ws", func(r chi.Router) {
			sshProxy.RegisterRoutes(r)
			sandboxHandler.RegisterRoutes(r)
		})
	}

	// Sandbox status endpoint (public — container health is not sensitive)
	r.Get("/api/v1/sandbox/status", sandboxHandler.HandleStatus)

	// API v1
	r.Route("/api/v1", func(r chi.Router) {
		// Public routes
		r.Get("/tracks", NewExamHandler(examUC).ListTracks)
		r.Get("/tracks/{slug}", NewExamHandler(examUC).GetTrack)
		r.Get("/tracks/{slug}/exams", NewExamHandler(examUC).ListExams)

		// Auth routes
		r.Post("/auth/register", NewAuthHandler(authUC).Register)
		r.Post("/auth/login", NewAuthHandler(authUC).Login)
		if appEnv == "development" {
			r.Post("/auth/dev-login", NewAuthHandler(authUC).DevLogin)
		}

		// Protected routes
		r.Group(func(r chi.Router) {
			r.Use(authMw.Authenticate)

			// User
			r.Get("/users/me", NewAuthHandler(authUC).GetProfile)
			r.Patch("/users/me", NewAuthHandler(authUC).UpdateProfile)
			r.Put("/users/me/preferences", NewAuthHandler(authUC).UpdatePreferences)
			r.Put("/users/me/email", NewAuthHandler(authUC).UpdateEmail)

			// Exams
			r.Get("/exams/{examId}", NewExamHandler(examUC).GetExam)
			r.Get("/exams/{examId}/questions", NewExamHandler(examUC).GetExamQuestions)

			// Attempts
			r.Post("/attempts", NewExamHandler(examUC).StartAttempt)
			r.Get("/attempts/{attemptId}", NewExamHandler(examUC).GetAttempt)
			r.Get("/attempts/{attemptId}/questions", NewExamHandler(examUC).GetAttemptQuestions)
			r.Get("/attempts/{attemptId}/details", NewExamHandler(examUC).GetAttemptWithDetails)
			r.Post("/attempts/{attemptId}/answers", NewExamHandler(examUC).SubmitAnswer)
			r.Post("/attempts/{attemptId}/complete", NewExamHandler(examUC).CompleteAttempt)
			r.Get("/attempts/history", NewExamHandler(examUC).GetHistory)

			// Explanations
			explanationHandler := NewExplanationHandler(explanationUC)
			r.Get("/explanations/{questionId}", explanationHandler.GetExplanation)
			r.Get("/explanations/{questionId}/versions", explanationHandler.GetExplanationVersion)
			r.Post("/explanations/telemetry/batch", explanationHandler.BatchSendTelemetry)

			// Labs
			if labUC != nil {
				labHandler := NewLabHandler(labUC)
				r.Get("/labs", labHandler.ListLabs)
				r.Get("/labs/active", labHandler.GetActiveSubmissions)
				r.Get("/labs/{labId}", labHandler.GetLab)
				r.Post("/labs/start", labHandler.StartLab)
				r.Get("/labs/submissions/{submissionId}", labHandler.GetSubmission)
				r.Post("/labs/submissions/{submissionId}/stop", labHandler.StopLab)
				r.Post("/labs/submissions/{submissionId}/pause", labHandler.PauseLab)
				r.Post("/labs/submissions/{submissionId}/resume", labHandler.ResumeLab)
				r.Post("/labs/submissions/{submissionId}/submit-module", labHandler.SubmitModule)
				r.Get("/labs/submissions/{submissionId}/scores", labHandler.GetScores)
			}

			// Study Progress
			if studyProgressUC != nil {
				studyHandler := NewStudyProgressHandler(studyProgressUC)
				r.Get("/study/progress", studyHandler.GetProgress)
				r.Post("/study/progress/toggle", studyHandler.ToggleGuide)
			}
		})
	})

	return r
}

// parseCORSOrigins parses a comma-separated env var string into a slice of
// allowed origins. Falls back to dev defaults if the env var is empty.
func parseCORSOrigins(envVal string) []string {
	defaults := []string{"http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"}
	if envVal == "" {
		return defaults
	}
	parts := strings.Split(envVal, ",")
	var origins []string
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p != "" {
			origins = append(origins, p)
		}
	}
	if len(origins) == 0 {
		return defaults
	}
	return origins
}
