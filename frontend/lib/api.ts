// Use Next.js proxy (/api/* → backend) to avoid CORS issues in the browser
const API_BASE = "/api";

interface RequestOptions {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
}

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, headers = {} } = options;

  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    // Handle 401 — token expired or invalid
    if (response.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        // Redirect to login if not already there
        if (!window.location.pathname.startsWith("/auth/")) {
          window.location.href = "/auth/login";
        }
      }
    }

    // Try to parse error body
    let errorMessage: string;
    try {
      const errorBody = await response.json();
      errorMessage = errorBody.error || errorBody.message || errorBody.detail || `HTTP ${response.status}`;
    } catch {
      // If JSON parsing fails, try plain text
      try {
        errorMessage = await response.text();
      } catch {
        errorMessage = `Request failed with status ${response.status}`;
      }
    }
    throw new ApiError(errorMessage, response.status);
  }

  return response.json();
}

// Auth API
export const authApi = {
  register: (data: { email: string; password: string; display_name: string }) =>
    request<{
      user: any;
      access_token: string;
      refresh_token: string;
      expires_in: number;
    }>("/auth/register", { method: "POST", body: data }),

  login: (data: { email: string; password: string }) =>
    request<{
      user: any;
      access_token: string;
      refresh_token: string;
      expires_in: number;
    }>("/auth/login", { method: "POST", body: data }),

  getProfile: () => request<any>("/users/me"),

  updateProfile: (data: { display_name?: string; avatar_url?: string | null }) =>
    request<any>("/users/me", { method: "PATCH", body: data }),

  updatePreferences: (data: { language?: string; theme?: string; notifications?: Record<string, boolean> }) =>
    request<any>("/users/me/preferences", { method: "PUT", body: data }),

  updateEmail: (data: { email: string }) =>
    request<any>("/users/me/email", { method: "PUT", body: data }),
};

// Tracks API
export const tracksApi = {
  list: () => request<any[]>("/tracks"),
  get: (slug: string) => request<any>(`/tracks/${slug}`),
  getExams: (slug: string) => request<any[]>(`/tracks/${slug}/exams`),
};

// Exams API
export const examsApi = {
  get: (examId: string) => request<any>(`/exams/${examId}`),
  getQuestions: (examId: string, lang?: string) => {
    const query = lang ? `?lang=${lang}` : '';
    return request<any[]>(`/exams/${examId}/questions${query}`);
  },
};

// Study Progress API
export const studyProgressApi = {
  getProgress: () => request<any[]>("/study/progress"),

  toggleGuide: (data: { guide_id: string; completed: boolean }) =>
    request<any>("/study/progress/toggle", { method: "POST", body: data }),
};

// Explanations API (Knowledge Base)
export const explanationsApi = {
  get: (questionId: string) =>
    request<any>(`/explanations/${questionId}`),

  getVersions: (questionId: string) =>
    request<any[]>(`/explanations/${questionId}/versions`),

  sendTelemetry: (events: any[]) =>
    request<any>("/explanations/telemetry/batch", { method: "POST", body: { events } }),
};

// Attempts API
export const attemptsApi = {
  start: (data: { exam_id: string; mode: string; shuffle_questions?: boolean }) =>
    request<any>("/attempts", { method: "POST", body: data }),

  get: (attemptId: string) => request<any>(`/attempts/${attemptId}`),

  getQuestions: (attemptId: string) => request<any[]>(`/attempts/${attemptId}/questions`),

  getDetails: (attemptId: string) => request<any>(`/attempts/${attemptId}/details`),

  submitAnswer: (attemptId: string, data: { question_id: string; answer: string; time_spent_seconds: number; was_flagged: boolean }) =>
    request<any>(`/attempts/${attemptId}/answers`, { method: "POST", body: data }),

  complete: (attemptId: string) =>
    request<any>(`/attempts/${attemptId}/complete`, { method: "POST" }),

  history: () => request<any[]>("/attempts/history"),
};

// Labs API
export const labsApi = {
  list: (trackId: string) =>
    request<any[]>(`/labs?track_id=${trackId}`),

  get: (labId: string) =>
    request<any>(`/labs/${labId}`),

  getActive: () =>
    request<any[]>("/labs/active"),

  start: (data: { lab_id: string; mode: string }) =>
    request<any>("/labs/start", { method: "POST", body: data }),

  getSubmission: (submissionId: string) =>
    request<any>(`/labs/submissions/${submissionId}`),

  stopSubmission: (submissionId: string) =>
    request<any>(`/labs/submissions/${submissionId}/stop`, { method: "POST" }),

  getScores: (submissionId: string) =>
    request<any[]>(`/labs/submissions/${submissionId}/scores`),
};

// Quick Labs API
export const quickLabsApi = {
  list: (trackId?: string) =>
    request<any[]>(`/quick-labs${trackId ? `?track_id=${trackId}` : ""}`),

  get: (labId: string) =>
    request<any>(`/quick-labs/${labId}`),
};
