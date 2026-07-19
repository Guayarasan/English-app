import { useState } from "react";

/**
 * Pide al usuario escribir su propia oración con la palabra. La
 * validación del backend es permisiva (ver exercise_service.check_writing):
 * solo exige que la palabra aparezca y que sea una oración real, no
 * gramática perfecta.
 */
export default function WritingExercise({ word, onSubmit, onContinue }) {
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (result) return;
    const res = await onSubmit({ userAnswer: answer });
    setResult(res);
  }

  function handleContinue() {
    setAnswer("");
    setResult(null);
    onContinue(result);
  }

  return (
    <div className="ticket w-full max-w-sm px-6 py-8 flex flex-col items-center gap-4">
      <span className="text-xs uppercase tracking-wide text-ink/50 dark:text-paper/50">
        Escribe una oración usando
      </span>
      <span className="font-display text-2xl">{word.text_en}</span>

      <form onSubmit={handleSubmit} className="w-full flex flex-col gap-3">
        <textarea
          autoFocus
          rows={3}
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          disabled={!!result}
          placeholder="Escribe tu oración en inglés..."
          className="px-4 py-3 rounded-card border border-ink/20 dark:border-paper/20 bg-transparent focus:outline-none focus:border-stamp-teal disabled:opacity-60 resize-none"
        />

        {result && (
          <p
            className={`text-sm text-center ${
              result.is_correct ? "text-stamp-teal" : "text-stamp-coral"
            }`}
          >
            {result.is_correct
              ? "¡Bien hecho!"
              : `Intenta usar la palabra "${word.text_en}" en una oración de al menos 3 palabras.`}
          </p>
        )}

        {!result ? (
          <button
            type="submit"
            className="py-3 rounded-card bg-ink text-paper dark:bg-paper dark:text-ink font-medium hover:opacity-90 transition"
          >
            Comprobar
          </button>
        ) : (
          <button
            type="button"
            onClick={handleContinue}
            className="py-3 rounded-card bg-stamp-teal text-paper font-medium hover:opacity-90 transition"
          >
            Continuar
          </button>
        )}
      </form>
    </div>
  );
}
