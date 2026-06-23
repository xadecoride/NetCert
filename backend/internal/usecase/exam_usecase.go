package usecase

import (
	"context"
	"errors"
	"fmt"
	"math/rand"
	"strings"
	"time"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

var (
	ErrAttemptNotFound = errors.New("attempt not found")
	ErrExamNotFound    = errors.New("exam not found")
)

type ExamUseCase struct {
	examRepo    domain.ExamRepository
	attemptRepo domain.AttemptRepository
}

func NewExamUseCase(examRepo domain.ExamRepository, attemptRepo domain.AttemptRepository) *ExamUseCase {
	return &ExamUseCase{examRepo: examRepo, attemptRepo: attemptRepo}
}

func (uc *ExamUseCase) ListTracks(ctx context.Context) ([]domain.Track, error) {
	return uc.examRepo.ListTracks(ctx)
}

func (uc *ExamUseCase) GetTrack(ctx context.Context, slug string) (*domain.Track, error) {
	return uc.examRepo.FindTrackBySlug(ctx, slug)
}

func (uc *ExamUseCase) ListExams(ctx context.Context, trackID uuid.UUID) ([]domain.Exam, error) {
	return uc.examRepo.ListExams(ctx, trackID)
}

func (uc *ExamUseCase) GetExam(ctx context.Context, examID uuid.UUID) (*domain.Exam, error) {
	return uc.examRepo.FindExamByID(ctx, examID)
}

func (uc *ExamUseCase) GetExamQuestions(ctx context.Context, examID uuid.UUID, lang string) ([]domain.Question, error) {
	questions, err := uc.examRepo.ListQuestions(ctx, examID)
	if err != nil {
		return nil, err
	}

	// Strip correct answers from options — client must never receive is_correct
	for i := range questions {
		for j := range questions[i].Options {
			questions[i].Options[j].IsCorrect = false
		}
	
	}

	return questions, nil
}

func (uc *ExamUseCase) StartAttempt(ctx context.Context, userID uuid.UUID, req domain.StartAttemptRequest) (*domain.Attempt, error) {
	exam, err := uc.examRepo.FindExamByID(ctx, req.ExamID)
	if err != nil {
		return nil, ErrExamNotFound
	}

	// Get all question IDs from the bank
	allIDs, err := uc.examRepo.ListQuestionIDs(ctx, req.ExamID)
	if err != nil {
		return nil, err
	}
	if len(allIDs) == 0 {
		return nil, errors.New("no questions available for this exam")
	}

	// Determine how many questions to take for this attempt
	// Exam mode: use exam's total_questions (realistic count, e.g. 60 for JNCIA)
	// Practice mode: use exam's total_questions too, but allow user to specify custom count
	targetCount := exam.TotalQuestions
	if req.QuestionCount > 0 && req.QuestionCount < targetCount {
		targetCount = req.QuestionCount
	}
	if targetCount > len(allIDs) {
		targetCount = len(allIDs)
	}

	// Enforce a minimum number of topology/diagram questions per exam type.
	minTopology := minTopologyQuestions(exam.Code)

	// Fetch topology question IDs separately so we can guarantee the minimum.
	var topologyIDs []uuid.UUID
	if minTopology > 0 {
		topologyIDs, err = uc.examRepo.ListQuestionIDsByType(ctx, req.ExamID, string(domain.QuestionTypeTopology))
		if err != nil {
			return nil, err
		}
	}

	otherIDs := make([]uuid.UUID, 0, len(allIDs))
	if len(topologyIDs) > 0 {
		topologySet := make(map[uuid.UUID]struct{}, len(topologyIDs))
		for _, id := range topologyIDs {
			topologySet[id] = struct{}{}
		}
		for _, id := range allIDs {
			if _, ok := topologySet[id]; !ok {
				otherIDs = append(otherIDs, id)
			}
		}
	} else {
		otherIDs = allIDs
	}

	// Randomly select the required topology count, then fill the rest with other questions.
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))

	topologyCount := minTopology
	if topologyCount > len(topologyIDs) {
		topologyCount = len(topologyIDs)
	}
	if topologyCount > targetCount {
		topologyCount = targetCount
	}

	otherCount := targetCount - topologyCount
	if otherCount > len(otherIDs) {
		otherCount = len(otherIDs)
		// If there are not enough other questions, use any remaining topology questions.
		topologyCount = targetCount - otherCount
		if topologyCount > len(topologyIDs) {
			topologyCount = len(topologyIDs)
		}
	}

	selected := make([]uuid.UUID, 0, targetCount)
	selected = append(selected, sampleIDs(rng, topologyIDs, topologyCount)...)
	selected = append(selected, sampleIDs(rng, otherIDs, otherCount)...)
	rng.Shuffle(len(selected), func(i, j int) {
		selected[i], selected[j] = selected[j], selected[i]
	})

	now := time.Now()
	attempt := &domain.Attempt{
		ID:                uuid.New(),
		UserID:            userID,
		ExamID:            req.ExamID,
		Status:            domain.AttemptStatusInProgress,
		Mode:              req.Mode,
		StartedAt:         now,
		DurationSeconds:   exam.DurationMinutes * 60,
		QuestionsTotal:    targetCount,
		QuestionsAnswered: 0,
		QuestionsCorrect:  0,
		CreatedAt:         now,
	}

	if err := uc.attemptRepo.Create(ctx, attempt); err != nil {
		return nil, err
	}

	// Save the selected question IDs
	if err := uc.attemptRepo.SaveAttemptQuestions(ctx, attempt.ID, selected); err != nil {
		return nil, err
	}

	return attempt, nil
}

// minTopologyQuestions returns the minimum number of diagram/topology questions
// that must appear in each attempt for the given exam code.
func minTopologyQuestions(code string) int {
	upper := strings.ToUpper(code)
	switch {
	case strings.HasPrefix(upper, "CCNA"):
		return 15
	case strings.HasPrefix(upper, "JN"):
		return 5
	default:
		return 0
	}
}

// sampleIDs returns a random subset of up to n IDs from ids.
func sampleIDs(rng *rand.Rand, ids []uuid.UUID, n int) []uuid.UUID {
	if n <= 0 {
		return nil
	}
	if n >= len(ids) {
		result := make([]uuid.UUID, len(ids))
		copy(result, ids)
		rng.Shuffle(len(result), func(i, j int) {
			result[i], result[j] = result[j], result[i]
		})
		return result
	}
	shuffled := make([]uuid.UUID, len(ids))
	copy(shuffled, ids)
	rng.Shuffle(len(shuffled), func(i, j int) {
		shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
	})
	return shuffled[:n]
}

func (uc *ExamUseCase) GetAttempt(ctx context.Context, attemptID uuid.UUID) (*domain.Attempt, error) {
	return uc.attemptRepo.FindByID(ctx, attemptID)
}

func (uc *ExamUseCase) GetAttemptQuestions(ctx context.Context, attemptID uuid.UUID) ([]domain.Question, error) {
	// Validate attempt exists
	_, err := uc.attemptRepo.FindByID(ctx, attemptID)
	if err != nil {
		return nil, ErrAttemptNotFound
	}

	// Get only the questions selected for this attempt
	questionIDs, err := uc.attemptRepo.GetAttemptQuestionIDs(ctx, attemptID)
	if err != nil {
		return nil, err
	}

	questions, err := uc.examRepo.GetQuestionsByIDs(ctx, questionIDs)
	if err != nil {
		return nil, err
	}

	// Hide correct answers — client must never receive is_correct during active attempt
	for i := range questions {
		for j := range questions[i].Options {
			questions[i].Options[j].IsCorrect = false
		}
	}

	return questions, nil
}

func (uc *ExamUseCase) SubmitAnswer(ctx context.Context, attemptID uuid.UUID, userID uuid.UUID, req domain.SubmitAnswerRequest) (*domain.AttemptAnswer, error) {
	attempt, err := uc.attemptRepo.FindByID(ctx, attemptID)
	if err != nil {
		return nil, ErrAttemptNotFound
	}

	if attempt.UserID != userID {
		return nil, errors.New("unauthorized")
	}

	if attempt.Status != domain.AttemptStatusInProgress {
		return nil, errors.New("attempt is not in progress")
	}

	// Prevent duplicate answers: check if this question was already answered
	hasAnswer, err := uc.attemptRepo.HasAnswer(ctx, attemptID, req.QuestionID)
	if err != nil {
		return nil, errors.New("failed to check existing answer")
	}
	if hasAnswer {
		return nil, errors.New("question already answered")
	}

	// Validate that the answered question belongs to this attempt's selected subset
	isInAttempt, err := uc.attemptRepo.IsQuestionInAttempt(ctx, attemptID, req.QuestionID)
	if err != nil {
		return nil, errors.New("failed to validate question")
	}
	if !isInAttempt {
		return nil, errors.New("question is not part of this attempt")
	}

	question, err := uc.examRepo.FindQuestionByID(ctx, req.QuestionID)
	if err != nil {
		return nil, errors.New("question not found")
	}

	isCorrect := checkAnswer(question, req.Answer)

	answer := &domain.AttemptAnswer{
		ID:               uuid.New(),
		AttemptID:        attemptID,
		QuestionID:       req.QuestionID,
		UserAnswer:       req.Answer,
		IsCorrect:        &isCorrect,
		TimeSpentSeconds: req.TimeSpentSeconds,
		WasFlagged:       req.WasFlagged,
		CreatedAt:        time.Now(),
	}

	if err := uc.attemptRepo.SaveAnswer(ctx, answer); err != nil {
		return nil, err
	}

	// Update attempt progress
	correctCount := attempt.QuestionsCorrect
	if isCorrect {
		correctCount++
	}
	if err := uc.attemptRepo.UpdateProgress(ctx, attemptID, attempt.QuestionsAnswered+1, correctCount); err != nil {
		return nil, fmt.Errorf("update progress: %w", err)
	}

	return answer, nil
}

func (uc *ExamUseCase) CompleteAttempt(ctx context.Context, attemptID uuid.UUID, userID uuid.UUID) (*domain.Attempt, error) {
	attempt, err := uc.attemptRepo.FindByID(ctx, attemptID)
	if err != nil {
		return nil, ErrAttemptNotFound
	}

	if attempt.UserID != userID {
		return nil, errors.New("unauthorized")
	}

	if attempt.Status == domain.AttemptStatusCompleted || attempt.Status == domain.AttemptStatusTimedOut {
		return nil, errors.New("attempt already finished")
	}

	// Re-fetch the latest counters from the DB so we include all submitted answers.
	// The in-memory attempt object was loaded before any answers were saved.
	fresh, err := uc.attemptRepo.FindByID(ctx, attemptID)
	if err != nil {
		return nil, err
	}

	score := 0.0
	if fresh.QuestionsTotal > 0 {
		score = float64(fresh.QuestionsCorrect) / float64(fresh.QuestionsTotal) * 100
	}

	if err := uc.attemptRepo.Complete(ctx, attemptID, score, fresh.QuestionsCorrect, fresh.QuestionsAnswered); err != nil {
		return nil, err
	}

	return uc.attemptRepo.FindByID(ctx, attemptID)
}

func (uc *ExamUseCase) GetAttemptWithDetails(ctx context.Context, attemptID uuid.UUID) (*domain.AttemptWithDetails, error) {
	attempt, err := uc.attemptRepo.FindByID(ctx, attemptID)
	if err != nil {
		return nil, ErrAttemptNotFound
	}

	exam, err := uc.examRepo.FindExamByID(ctx, attempt.ExamID)
	if err != nil {
		return nil, err
	}

	// Get only the questions selected for this attempt
	questionIDs, err := uc.attemptRepo.GetAttemptQuestionIDs(ctx, attemptID)
	if err != nil {
		return nil, err
	}

	questions, err := uc.examRepo.GetQuestionsByIDs(ctx, questionIDs)
	if err != nil {
		return nil, err
	}

	// Get user answers for this attempt
	answers, err := uc.attemptRepo.GetAnswers(ctx, attemptID)
	if err != nil {
		return nil, err
	}

	// Build answer lookup: questionID -> AttemptAnswer
	answerMap := make(map[string]*domain.AttemptAnswer)
	for i := range answers {
		answerMap[answers[i].QuestionID.String()] = &answers[i]
	}

	// Build the detailed questions list
	detailed := make([]domain.AttemptQuestionWithAnswer, 0, len(questions))
	for _, q := range questions {
		qa := domain.AttemptQuestionWithAnswer{
			ID:               q.ID,
			Body:             q.Body,
			Options:          q.Options,
			QuestionType:     q.QuestionType,
			Difficulty:       q.Difficulty,
			Explanation:      q.Explanation,
			ReferenceURLs:    q.ReferenceURLs,
			BlueprintSection: q.BlueprintSection,
		}
		if ans, ok := answerMap[q.ID.String()]; ok {
			qa.UserAnswer = ans.UserAnswer
			qa.IsCorrect = ans.IsCorrect
			qa.WasFlagged = ans.WasFlagged
			qa.TimeSpentSeconds = ans.TimeSpentSeconds
		}
		detailed = append(detailed, qa)
	}

	return &domain.AttemptWithDetails{
		Attempt:      *attempt,
		ExamName:     exam.Name,
		ExamCode:     exam.Code,
		PassingScore: exam.PassingScore,
		Questions:    detailed,
	}, nil
}

func (uc *ExamUseCase) GetAttemptHistory(ctx context.Context, userID uuid.UUID) ([]domain.Attempt, error) {
	return uc.attemptRepo.ListByUser(ctx, userID)
}

func checkAnswer(question *domain.Question, answer string) bool {
	switch question.QuestionType {
	case domain.QuestionTypeFillBlank:
		// For fill-blank, compare user text against the correct option's text (case-insensitive)
		for _, opt := range question.Options {
			if opt.IsCorrect {
				return strings.EqualFold(strings.TrimSpace(answer), strings.TrimSpace(opt.Text))
			}
		}
		return false

	case domain.QuestionTypeMultipleChoice:
		// For multiple-choice, answer is comma-separated IDs like "a,b"
		selectedIDs := strings.Split(answer, ",")
		// Build map of correct option IDs
		correctMap := make(map[string]bool)
		for _, opt := range question.Options {
			if opt.IsCorrect {
				correctMap[opt.ID] = true
			}
		}
		// Count correct selections
		correctCount := 0
		for _, id := range selectedIDs {
			id = strings.TrimSpace(id)
			if id == "" {
				continue
			}
			if correctMap[id] {
				correctCount++
			}
		}
		// Must select ALL correct options and NO incorrect ones
		return correctCount == len(correctMap) && correctCount == len(selectedIDs)

	default:
		// Single-choice: match by option ID
		for _, opt := range question.Options {
			if opt.IsCorrect && opt.ID == answer {
				return true
			}
		}
		return false
	}
}

