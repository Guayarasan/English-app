import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(form);
      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail || "No se pudo iniciar sesión. Intenta de nuevo."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <h1 className="font-display text-3xl mb-1">Bienvenido de vuelta</h1>
        <p className="text-ink/60 dark:text-paper/60 mb-8">
          Tu pasaporte de inglés te espera.
        </p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <label htmlFor="email" className="sr-only">
            Correo electrónico
          </label>
          <input
            id="email"
            type="email"
            required
            placeholder="tu@email.com"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="px-4 py-3 rounded-card border border-ink/20 dark:border-paper/20 bg-transparent focus:outline-none focus:border-stamp-teal"
          />
          <label htmlFor="password" className="sr-only">
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            required
            placeholder="Contraseña"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            className="px-4 py-3 rounded-card border border-ink/20 dark:border-paper/20 bg-transparent focus:outline-none focus:border-stamp-teal"
          />

          {error && (
            <p role="alert" className="text-sm text-stamp-coral">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="mt-2 py-3 rounded-card bg-ink text-paper dark:bg-paper dark:text-ink font-medium hover:opacity-90 transition disabled:opacity-50"
          >
            {submitting ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <p className="mt-6 text-sm text-ink/60 dark:text-paper/60">
          ¿No tienes cuenta?{" "}
          <Link to="/register" className="text-stamp-teal font-medium">
            Crea una
          </Link>
        </p>
      </div>
    </div>
  );
}
