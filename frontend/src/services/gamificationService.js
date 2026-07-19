import { api } from "./api";

export async function fetchAchievements() {
  const { data } = await api.get("/api/achievements");
  return data;
}

export async function fetchTodayChallenges() {
  const { data } = await api.get("/api/challenges/today");
  return data;
}
