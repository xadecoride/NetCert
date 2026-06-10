package usecase

import (
	"context"
	"errors"
	"testing"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// mockExamRepository is a test double for domain.ExamRepository.
type mockExamRepository struct {
	tracks      []domain.Track
	exams       map[uuid.UUID]*domain.Exam
	questions   map[uuid.UUID][]domain.Question
	questionIDs map[uuid.UUID][]uuid.UUID
}

func newMockExamRepository() *mockExamRepository {
	return &mockExamRepository{
		exams:       make(map[uuid.UUID]*domain.Exam),
		questions:   make(map[uuid.UUID][]domain.Question),
		questionIDs: make(map[uuid.UUID][]uuid.UUID),
	}
}

func (m *mockExamRepository) ListTracks(ctx context.Context) ([]domain.Track, error) {
	return m.tracks, nil
}

func (m *mockExamRepository) FindTrackBySlug(ctx context.Context, slug string) (*domain.Track, error) {
	for _, t := range m.tracks {
		if t.Slug == slug {
			return &t, nil
		}
	}
	return nil, errors.New("track not found")
}

func (m *mockExamRepository) ListExams(ctx context.Context, trackID uuid.UUID) ([]domain.Exam, error) {
	var result []domain.Exam
	for _, e := range m.exams {
		if e.TrackID == trackID {
			result = append(result, *e)
		}
	}
	return result, nil
}

func (m *mockExamRepository) FindExamByID(ctx context.Context, id uuid.UUID) (*domain.Exam, error) {
	if e, ok := m.exams[id]; ok {
		return e, nil
	}
	return nil, errors.New("exam not found")
}

func (m *mockExamRepository) ListQuestions(ctx context.Context, examID uuid.UUID) ([]domain.Question, error) {
	return m.questions[examID], nil
}

func (m *mockExamRepository) ListQuestionIDs(ctx context.Context, examID uuid.UUID) ([]uuid.UUID, error) {
	return m.questionIDs[examID], nil
}

func (m *mockExamRepository) GetQuestionsByIDs(ctx context.Context, ids []uuid.UUID) ([]domain.Question, error) {
	var result []domain.Question
	for _, examQs := range m.questions {
		for _, q := range examQs {
			for _, id := range ids {
				if q.ID == id {
					result = append(result, q)
				}
			}
		}
	}
	return result, nil
}

func (m *mockExamRepository) FindQuestionByID(ctx context.Context, id uuid.UUID) (*domain.Question, error) {
	for _, examQs := range m.questions {
		for _, q := range examQs {
			if q.ID == id {
				return &q, nil
			}
		}
	}
	return nil, errors.New("question not found")
}

// mockAttemptRepository is a test double for domain.AttemptRepository.
type mockAttemptRepository struct {
	attempts map[uuid.UUID]*domain.Attempt
	answers  map[uuid.UUID][]domain.AttemptAnswer
}

func newMockAttemptRepository() *mockAttemptRepository {
	return &mockAttemptRepository{
		attempts: make(map[uuid.UUID]*domain.Attempt),
		answers:  make(map[uuid.UUID][]domain.AttemptAnswer),
	}
}

func (m *mockAttemptRepository) Create(ctx context.Context, a *domain.Attempt) error {
	m.attempts[a.ID] = a
	return nil
}

func (m *mockAttemptRepository) FindByID(ctx context.Context, id uuid.UUID) (*domain.Attempt, error) {
	if a, ok := m.attempts[id]; ok {
		return a, nil
	}
	return nil, errors.New("attempt not found")
}

func (m *mockAttemptRepository) ListByUser(ctx context.Context, userID uuid.UUID) ([]domain.Attempt, error) {
	var result []domain.Attempt
	for _, a := range m.attempts {
		if a.UserID == userID {
			result = append(result, *a)
		}
	}
	return result, nil
}

func (m *mockAttemptRepository) UpdateStatus(ctx context.Context, id uuid.UUID, status domain.AttemptStatus) error {
	if a, ok := m.attempts[id]; ok {
		a.Status = status
	}
	return nil
}

func (m *mockAttemptRepository) Complete(ctx context.Context, id uuid.UUID, score float64, correct, answered int) error {
	if a, ok := m.attempts[id]; ok {
		a.Status = domain.AttemptStatusCompleted
		a.Score = &score
		a.QuestionsCorrect = correct
		a.QuestionsAnswered = answered
	}
	return nil
}

func (m *mockAttemptRepository) UpdateProgress(ctx context.Context, id uuid.UUID, answered, correct int) error {
	if a, ok := m.attempts[id]; ok {
		a.QuestionsAnswered = answered
		a.QuestionsCorrect = correct
	}
	return nil
}

func (m *mockAttemptRepository) SaveAnswer(ctx context.Context, a *domain.AttemptAnswer) error {
	m.answers[a.AttemptID] = append(m.answers[a.AttemptID], *a)
	return nil
}

func (m *mockAttemptRepository) GetAnswers(ctx context.Context, attemptID uuid.UUID) ([]domain.AttemptAnswer, error) {
	return m.answers[attemptID], nil
}

func (m *mockAttemptRepository) SaveAttemptQuestions(ctx context.Context, attemptID uuid.UUID, questionIDs []uuid.UUID) error {
	return nil
}

func (m *mockAttemptRepository) GetAttemptQuestionIDs(ctx context.Context, attemptID uuid.UUID) ([]uuid.UUID, error) {
	return nil, nil
}

func (m *mockAttemptRepository) IsQuestionInAttempt(ctx context.Context, attemptID, questionID uuid.UUID) (bool, error) {
	return true, nil
}

func (m *mockAttemptRepository) HasUserAnsweredQuestion(ctx context.Context, questionID, userID uuid.UUID) (bool, error) {
	return false, nil
}

func (m *mockAttemptRepository) HasAnswer(ctx context.Context, attemptID, questionID uuid.UUID) (bool, error) {
	for _, ans := range m.answers[attemptID] {
		if ans.QuestionID == questionID {
			return true, nil
		}
	}
	return false, nil
}

func TestExamUseCase_StartAttempt(t *testing.T) {
	examRepo := newMockExamRepository()
	attemptRepo := newMockAttemptRepository()
	uc := NewExamUseCase(examRepo, attemptRepo)

	ctx := context.Background()
	userID := uuid.New()
	examID := uuid.New()

	examRepo.exams[examID] = &domain.Exam{
		ID:              examID,
		TrackID:         uuid.New(),
		Code:            "TEST-001",
		Name:            "Test Exam",
		Level:           domain.LevelJNCIA,
		DurationMinutes: 60,
		TotalQuestions:  10,
		PassingScore:    70,
		IsActive:        true,
	}

	qIDs := []uuid.UUID{uuid.New(), uuid.New(), uuid.New()}
	examRepo.questionIDs[examID] = qIDs
	for _, qid := range qIDs {
		examRepo.questions[examID] = append(examRepo.questions[examID], domain.Question{
			ID:       qid,
			ExamID:   examID,
			Body:     "Test question",
			Options:  []domain.QuestionOption{{ID: "a", Text: "A", IsCorrect: true}, {ID: "b", Text: "B", IsCorrect: false}},
			Difficulty: 1,
		})
	}

	attempt, err := uc.StartAttempt(ctx, userID, domain.StartAttemptRequest{
		ExamID:        examID,
		Mode:          "practice",
		QuestionCount: 0,
	})
	require.NoError(t, err)
	assert.Equal(t, domain.AttemptStatusInProgress, attempt.Status)
	assert.Equal(t, userID, attempt.UserID)
	assert.Equal(t, examID, attempt.ExamID)
	assert.Equal(t, len(qIDs), attempt.QuestionsTotal)
}

func TestExamUseCase_SubmitAnswer(t *testing.T) {
	examRepo := newMockExamRepository()
	attemptRepo := newMockAttemptRepository()
	uc := NewExamUseCase(examRepo, attemptRepo)

	ctx := context.Background()
	userID := uuid.New()
	examID := uuid.New()
	attemptID := uuid.New()
	questionID := uuid.New()

	attemptRepo.attempts[attemptID] = &domain.Attempt{
		ID:                attemptID,
		UserID:            userID,
		ExamID:            examID,
		Status:            domain.AttemptStatusInProgress,
		QuestionsTotal:    1,
		QuestionsAnswered: 0,
		QuestionsCorrect:  0,
	}

	examRepo.questions[examID] = []domain.Question{
		{
			ID:         questionID,
			ExamID:     examID,
			Body:       "What is 2+2?",
			QuestionType: domain.QuestionTypeSingleChoice,
			Options: []domain.QuestionOption{
				{ID: "a", Text: "3", IsCorrect: false},
				{ID: "b", Text: "4", IsCorrect: true},
			},
		},
	}

	// Correct answer
	answer, err := uc.SubmitAnswer(ctx, attemptID, userID, domain.SubmitAnswerRequest{
		QuestionID: questionID,
		Answer:     "b",
	})
	require.NoError(t, err)
	assert.NotNil(t, answer.IsCorrect)
	assert.True(t, *answer.IsCorrect)

	// Duplicate answer should fail
	_, err = uc.SubmitAnswer(ctx, attemptID, userID, domain.SubmitAnswerRequest{
		QuestionID: questionID,
		Answer:     "b",
	})
	assert.Error(t, err)
}

func TestCheckAnswer(t *testing.T) {
	q := &domain.Question{
		QuestionType: domain.QuestionTypeSingleChoice,
		Options: []domain.QuestionOption{
			{ID: "a", Text: "Option A", IsCorrect: true},
			{ID: "b", Text: "Option B", IsCorrect: false},
		},
	}
	assert.True(t, checkAnswer(q, "a"))
	assert.False(t, checkAnswer(q, "b"))

	// fill-blank
	q2 := &domain.Question{
		QuestionType: domain.QuestionTypeFillBlank,
		Options: []domain.QuestionOption{
			{ID: "ans", Text: "Junos", IsCorrect: true},
		},
	}
	assert.True(t, checkAnswer(q2, "junos"))
	assert.False(t, checkAnswer(q2, "cisco"))

	// multiple-choice
	q3 := &domain.Question{
		QuestionType: domain.QuestionTypeMultipleChoice,
		Options: []domain.QuestionOption{
			{ID: "a", Text: "A", IsCorrect: true},
			{ID: "b", Text: "B", IsCorrect: true},
			{ID: "c", Text: "C", IsCorrect: false},
		},
	}
	assert.True(t, checkAnswer(q3, "a,b"))
	assert.False(t, checkAnswer(q3, "a,c"))
}
