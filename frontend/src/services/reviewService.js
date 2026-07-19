import { api } from "./api";

export async function fetchDueWords(limit = 15) {
  const { data } = await api.get("/api/review/due", { params: { limit } });
  return data;
}

export async function submitAnswer({ wordId, exerciseType, isCorrect, userAnswer, direction }) {
  const { data } = await api.post("/api/review/answer", {
    word_id: wordId,
    exercise_type: exerciseType,
    is_correct: isCorrect ?? null,
    user_answer: userAnswer ?? null,
    direction: direction ?? "en_to_es",
  });
  return data;
}
