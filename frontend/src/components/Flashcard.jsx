import { useState } from "react";
import { motion } from "framer-motion";

/**
 * Flashcard estilo "postal": frente = palabra en inglés, dorso = traducción
 * + ejemplo. Voltea en 3D al hacer click, coherente con la metáfora de
 * viaje/pasaporte del resto de la app.
 *
 * onAnswer(wasCorrect) es opcional: si se pasa, aparecen dos botones de
 * autoevaluación en el dorso ("no la sabía" / "la sabía") que alimentan
 * el motor de repaso espaciado.
 */
export default function Flashcard({ word, onAnswer }) {
  const [flipped, setFlipped] = useState(false);

  function handleAnswer(wasCorrect, e) {
    e.stopPropagation();
    onAnswer?.(wasCorrect);
    setFlipped(false);
  }

  return (
    <div
      className="w-full max-w-72 h-44 cursor-pointer select-none"
      style={{ perspective: "1200px" }}
      onClick={() => setFlipped((f) => !f)}
      role="button"
      tabIndex={0}
      aria-label={`Tarjeta de la palabra ${word.text_en}. Presiona para ver la traducción.`}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          setFlipped((f) => !f);
        }
      }}
    >
      <motion.div
        className="relative w-full h-full"
        style={{ transformStyle: "preserve-3d" }}
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.5, ease: "easeInOut" }}
      >
        {/* Frente */}
        <div
          className="absolute inset-0 rounded-card border border-ink/15 dark:border-paper/15 bg-paper dark:bg-ink-light flex flex-col items-center justify-center gap-2 shadow-sm"
          style={{ backfaceVisibility: "hidden" }}
        >
          <span className="font-display text-3xl">{word.text_en}</span>
          <span className="text-xs text-ink/50 dark:text-paper/50 uppercase tracking-wide">
            toca para traducir
          </span>
        </div>

        {/* Dorso */}
        <div
          className="absolute inset-0 rounded-card border border-stamp-teal/40 bg-stamp-teal/10 dark:bg-stamp-teal/20 flex flex-col items-center justify-center gap-2 px-4 text-center"
          style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)" }}
        >
          <span className="font-display text-2xl text-stamp-teal dark:text-paper">
            {word.text_es}
          </span>
          {word.example_sentence_en && (
            <span className="text-sm text-ink/70 dark:text-paper/70 italic">
              "{word.example_sentence_en}"
            </span>
          )}
          {onAnswer && (
            <div className="flex gap-2 mt-1">
              <button
                onClick={(e) => handleAnswer(false, e)}
                className="px-3 py-1.5 text-sm rounded-card bg-stamp-coral/15 text-stamp-coral font-medium hover:bg-stamp-coral/25 transition"
              >
                No la sabía
              </button>
              <button
                onClick={(e) => handleAnswer(true, e)}
                className="px-3 py-1.5 text-sm rounded-card bg-stamp-teal/15 text-stamp-teal font-medium hover:bg-stamp-teal/25 transition"
              >
                La sabía
              </button>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
