import { useMemo } from "react";
import Flashcard from "../Flashcard";
import TranslationExercise from "./TranslationExercise";
import FillBlankExercise from "./FillBlankExercise";
import WritingExercise from "./WritingExercise";

const EXERCISE_COMPONENTS = {
  translation: TranslationExercise,
  fill_blank: FillBlankExercise,
  writing: WritingExercise,
};

/**
 * Elige el tipo de ejercicio para una palabra de forma determinística
 * (basada en su id), para que no cambie entre re-renders del mismo
 * ítem de la cola. fill_blank y writing requieren una oración de
 * ejemplo; si la palabra no tiene, se cae a flashcard/translation.
 */
function pickExerciseType(word) {
  const sentence = word.example_sentence_en?.toLowerCase() ?? "";
  const pool = sentence
    ? ["flashcard", "translation", "fill_blank", "writing"]
    : ["flashcard", "translation"];
  // Si la palabra no aparece tal cual en la oración (ej. conjugada), fill_blank
  // no podría ocultarla y regalaría la respuesta.
  if (sentence && !sentence.includes(word.text_en.toLowerCase())) {
    return ["flashcard", "translation", "writing"][word.id % 3];
  }
  return pool[word.id % pool.length];
}

/**
 * Punto único desde el que el Dashboard pide ejercicios: recibe la
 * palabra actual, una función submitAnswer(payload) que llama al
 * backend, y onComplete(result) que se dispara cuando el usuario
 * termina de ver el feedback y está listo para la siguiente palabra.
 */
export default function ExerciseRenderer({ word, submitAnswer, onComplete }) {
  const exerciseType = useMemo(() => pickExerciseType(word), [word.id]);

  if (exerciseType === "flashcard") {
    return (
      <Flashcard
        word={word}
        onAnswer={async (wasCorrect) => {
          const result = await submitAnswer({
            wordId: word.id,
            exerciseType: "flashcard",
            isCorrect: wasCorrect,
          });
          onComplete(result);
        }}
      />
    );
  }

  const Component = EXERCISE_COMPONENTS[exerciseType];

  return (
    <Component
      word={word}
      onSubmit={(extra) =>
        submitAnswer({ wordId: word.id, exerciseType, ...extra })
      }
      onContinue={onComplete}
    />
  );
}
