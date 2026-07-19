/**
 * Estado vacío consistente: título + descripción opcional, dentro del
 * mismo motivo "ticket" que el resto de la app. Se usa cuando una
 * sección no tiene datos todavía (sin repaso pendiente, sin logros,
 * sin historial, etc.).
 */
export default function EmptyState({ title, description, icon = "🧭" }) {
  return (
    <div className="ticket px-6 py-8 text-center">
      <span className="text-2xl block mb-2" aria-hidden="true">
        {icon}
      </span>
      <p className="font-display text-lg mb-1">{title}</p>
      {description && (
        <p className="text-ink/60 dark:text-paper/60 text-sm">{description}</p>
      )}
    </div>
  );
}
