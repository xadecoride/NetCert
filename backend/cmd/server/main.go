package main

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"
	"github.com/netcert/backend/internal/config"
	delivery "github.com/netcert/backend/internal/delivery/http"
	jwtpkg "github.com/netcert/backend/internal/pkg/jwt"
	"github.com/netcert/backend/internal/repository/postgres"
	"github.com/netcert/backend/internal/usecase"
)

func main() {
	// Initialize structured JSON logging
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	}))
	slog.SetDefault(logger)

	// Load .env file if exists
	_ = godotenv.Load()

	cfg, err := config.Load()
	if err != nil {
		slog.Error("Failed to load config", slog.String("error", err.Error()))
		os.Exit(1)
	}

	// Database connection
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	pool, err := pgxpool.New(ctx, cfg.Database.DSN)
	if err != nil {
		slog.Error("Unable to connect to database", slog.String("error", err.Error()))
		os.Exit(1)
	}
	defer pool.Close()

	if err := pool.Ping(ctx); err != nil {
		slog.Warn("Database not reachable", slog.String("error", err.Error()))
		slog.Warn("Server will start, but database features will be unavailable")
	}

	// Initialize repositories
	userRepo := postgres.NewUserRepository(pool)
	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	explanationRepo := postgres.NewExplanationRepository(pool)
	labRepo := postgres.NewLabRepository(pool)
	studyProgressRepo := postgres.NewStudyProgressRepository(pool)

	// Initialize JWT manager
	jwtManager := jwtpkg.NewJWTManager(cfg.JWT.Secret, cfg.JWT.AccessTokenTTL, cfg.JWT.RefreshTokenTTL)

	// Initialize use cases
	authUC := usecase.NewAuthUseCase(userRepo, jwtManager)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	explanationUC := usecase.NewExplanationUseCase(explanationRepo, attemptRepo)
	labUC := usecase.NewLabUseCase(
		labRepo,
		getEnv("CLAB_BIN_PATH", "containerlab"),
		getEnv("CLAB_BASE_DIR", "/tmp/netcert-labs"),
		getEnv("CLAB_WS_HOST", "0.0.0.0"),
		getEnv("CLAB_WS_PORT", "8090"),
		getEnv("LABS_BASE_DIR", "/app/labs"),
		getEnv("DIND_CONTAINER", "netcert-staging-clab-dind"),
		getEnv("HOST_DOCKER_SOCKET", "/var/run/docker.sock"),
	)

	// Initialize study progress use case
	studyProgressUC := usecase.NewStudyProgressUseCase(studyProgressRepo)

	// Create router with all dependencies
	// WebSocket SSH proxy routes are mounted at /ws/ inside NewRouter
	router := delivery.NewRouter(authUC, examUC, explanationUC, labUC, studyProgressUC, jwtManager, getEnv("APP_ENV", "development"))

	// Create server
	srv := &http.Server{
		Addr:         fmt.Sprintf("%s:%s", cfg.Server.Host, cfg.Server.Port),
		Handler:      router,
		ReadTimeout:  cfg.Server.ReadTimeout,
		WriteTimeout: cfg.Server.WriteTimeout,
	}

	// Graceful shutdown
	go func() {
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
		<-sigCh
		slog.Info("Shutting down server...")
		shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer shutdownCancel()
		srv.Shutdown(shutdownCtx)
	}()

	slog.Info("NetCert API server starting", slog.String("host", cfg.Server.Host), slog.String("port", cfg.Server.Port))
	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		slog.Error("Server error", slog.String("error", err.Error()))
		os.Exit(1)
	}
	slog.Info("Server stopped")
}

// getEnv returns the value of an environment variable or a default value if not set.
func getEnv(key, defaultValue string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return defaultValue
}

// WebSocket SSH proxy is available on the main server at /ws/lab/{submissionID}/{deviceName}
