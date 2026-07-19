/**
 * Componente firma de la identidad visual: un "ticket de embarque"
 * con borde punteado y muescas circulares (ver .ticket en index.css).
 * Muestra la racha actual y el XP — se usa en el header y en el
 * dashboard.
 */
export default function StreakTicket({ streak, xp, level }) {
  return (
    <div className="ticket flex items-center gap-6 px-6 py-3 bg-paper dark:bg-ink-light">
      <div className="flex flex-col items-center">
        <span className="font-mono text-2xl font-bold text-stamp-coral">
          {streak}
        </span>
        <span className="text-[11px] uppercase tracking-wide text-ink/60 dark:text-paper/60">
          racha
        </span>
      </div>
      <div className="w-px h-8 bg-ink/15 dark:bg-paper/15" />
      <div className="flex flex-col items-center">
        <span className="font-mono text-2xl font-bold text-stamp-gold">
          {xp}
        </span>
        <span className="text-[11px] uppercase tracking-wide text-ink/60 dark:text-paper/60">
          xp
        </span>
      </div>
      <div className="w-px h-8 bg-ink/15 dark:bg-paper/15" />
      <div className="flex flex-col items-center">
        <span className="font-mono text-2xl font-bold text-stamp-teal">
          {level}
        </span>
        <span className="text-[11px] uppercase tracking-wide text-ink/60 dark:text-paper/60">
          nivel
        </span>
      </div>
    </div>
  );
}
