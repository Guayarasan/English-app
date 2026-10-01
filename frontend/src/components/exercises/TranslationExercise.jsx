import { useState } from "react";

/**
 * Ejercicio de traducción. La dirección (en->es o es->en) se decide
 * al azar por palabra para variar la práctica.
 */
export default function TranslationExercise({ word, onSubmit, onContinue }) {
  const [direction] = useState(() => (Math.random() > 0.5 ? "en_to_es" : "es_to_en"));
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const prompt = direction === "en_to_es" ? word.text_en : word.text_es;

  async function handleSubmit(e) {
    e.preventDefault();
    if (result || submitting) return;
    setError("");
    setSubmitting(true);
    try {
      const res = await onSubmit({ userAnswer: answer, direction });
      setResult(res);
    } catch {
      setError("No se pudo enviar tu respuesta. Revisa tu conexión e inténtalo de nuevo.");
    } finally {
      setSubmitting(false);
    }
  }

  function handleContinue() {
    setAnswer("");
    setResult(null);
    onContinue(result);
  }

  return (
    <div className="ticket w-full max-w-sm px-4 sm:px-6 py-6 sm:py-8 flex flex-col items-center gap-4">
      <span className="text-xs uppercase tracking-wide text-ink/50 dark:text-paper/50">
        Traduce
      </span>
      <span className="font-display text-2xl text-center">{prompt}</span>

      <form onSubmit={handleSubmit} className="w-full flex flex-col gap-3">
        <input
          autoFocus
          required
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          disabled={!!result}
          placeholder="Tu respuesta..."
          className="px-4 py-3 min-h-11 rounded-card border border-ink/20 dark:border-paper/20 bg-transparent text-center focus:outline-none focus:border-stamp-teal disabled:opacity-60"
        />

        {error && (
          <p role="alert" className="text-sm text-center text-stamp-coral">
            {error}
          </p>
        )}

        {result && (
          <p
            className={`text-sm text-center ${
              result.is_correct ? "text-stamp-teal" : "text-stamp-coral"
            }`}
          >
            {result.is_correct
              ? "¡Correcto!"
              : `La respuesta era: "${result.correct_answer}"`}
          </p>
        )}

        {!result ? (
          <button
            type="submit"
            disabled={submitting || !answer.trim()}
            className="py-3 min-h-11 rounded-card bg-ink text-paper dark:bg-paper dark:text-ink font-medium hover:opacity-90 transition disabled:opacity-50"
          >
            {submitting ? "Comprobando..." : "Comprobar"}
          </button>
        ) : (
          <button
            type="button"
            onClick={handleContinue}
            className="py-3 min-h-11 rounded-card bg-stamp-teal text-paper font-medium hover:opacity-90 transition"
          >
            Continuar
          </button>
        )}
      </form>
    </div>
  );
}
