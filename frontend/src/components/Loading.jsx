/**
 * Estado de carga consistente en toda la app: un ticket con animación
 * de pulso sutil, en vez de texto plano "Cargando..." repetido en cada
 * página. role="status" + aria-live para que los lectores de pantalla
 * lo anuncien sin interrumpir.
 */
export default function Loading({ label = "Cargando..." }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="ticket px-6 py-8 flex items-center justify-center animate-pulse"
    >
      <span className="text-sm text-ink/60 dark:text-paper/60">{label}</span>
    </div>
  );
}
