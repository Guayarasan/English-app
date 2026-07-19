import { api } from "./api";

export async function registerUser({ email, username, password }) {
  const { data } = await api.post("/api/auth/register", {
    email,
    username,
    password,
  });
  return data;
}

export async function loginUser({ email, password }) {
  const { data } = await api.post("/api/auth/login", { email, password });
  return data;
}

export async function fetchCurrentUser() {
  const { data } = await api.get("/api/auth/me");
  return data;
}
