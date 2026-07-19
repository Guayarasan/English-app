import { api } from "./api";

export async function fetchWords({ category, limit = 20 } = {}) {
  const { data } = await api.get("/api/words", { params: { category, limit } });
  return data;
}
