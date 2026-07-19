import { api } from "./api";

export async function fetchStatsSummary() {
  const { data } = await api.get("/api/stats/summary");
  return data;
}

export async function fetchStatsHistory(days = 30) {
  const { data } = await api.get("/api/stats/history", { params: { days } });
  return data;
}

export async function fetchCategoryStats() {
  const { data } = await api.get("/api/stats/categories");
  return data;
}

export async function fetchHardestWords(limit = 10) {
  const { data } = await api.get("/api/stats/hardest-words", { params: { limit } });
  return data;
}
