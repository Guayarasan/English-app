import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function clearSessionAndRedirect() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  if (window.location.pathname !== "/login") {
    window.location.href = "/login";
  }
}

// Varias peticiones pueden fallar con 401 a la vez; comparten un único
// intento de refresh en vez de gastar el refresh token varias veces.
let refreshPromise = null;

function refreshTokens() {
  if (!refreshPromise) {
    const refreshToken = localStorage.getItem("refresh_token");
    // Cliente aparte (sin interceptores) para que un fallo aquí no se reintente en bucle
    refreshPromise = axios
      .post(`${API_URL}/api/auth/refresh`, { refresh_token: refreshToken })
      .then(({ data }) => {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        return data.access_token;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

// Si el access token expiró se intenta renovar con el refresh token y se
// repite la petición original; solo si eso falla se limpia la sesión y se
// manda a login. No aplica a /api/auth/login ni /register, donde un 401
// es "credenciales incorrectas", no "sesión expirada".
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const url = original?.url || "";
    const isAuthEndpoint =
      url.includes("/api/auth/login") || url.includes("/api/auth/register");

    if (error.response?.status !== 401 || isAuthEndpoint || !original) {
      return Promise.reject(error);
    }

    if (!original._retried && localStorage.getItem("refresh_token")) {
      original._retried = true;
      try {
        const newToken = await refreshTokens();
        original.headers.Authorization = `Bearer ${newToken}`;
        return api(original);
      } catch {
        // cae al cierre de sesión de abajo
      }
    }

    clearSessionAndRedirect();
    return Promise.reject(error);
  }
);
