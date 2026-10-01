import { useMemo, useState } from "react";

/**
 * Muestra la oración de ejemplo con la palabra objetivo oculta.
 * Requiere que la palabra tenga example_sentence_en; el selector de
 * ejercicios (ExerciseRenderer) ya filtra por esto antes de mostrarlo.
 */
export default function FillBlankExercise({ word, onSubmit, onContinue }) {
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const blankedSentence = useMemo(() => {
    const escaped = word.text_en.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const re = new RegExp(escaped, "i");
    return word.example_sentence_en.replace(re, "_____");
  }, [word]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (result || submitting) return;
    setError("");
    setSubmitting(true);
    try {
      const res = await onSubmit({ userAnswer: answer });
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
        Completa la palabra
      </span>
      <span className="font-display text-lg text-center leading-relaxed">
        {blankedSentence}
      </span>

      <form onSubmit={handleSubmit} className="w-full flex flex-col gap-3">
        <input
          autoFocus
          required
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          disabled={!!result}
          placeholder="Palabra que falta..."
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
              : `La palabra era: "${result.correct_answer}"`}
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
