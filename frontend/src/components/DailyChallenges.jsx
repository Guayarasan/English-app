/**
 * Cada desafío se muestra como una fila con barra de progreso.
 * Cuando `completed` es true se marca en verde-tinta con un check.
 */
export default function DailyChallenges({ challenges }) {
  if (!challenges.length) return null;

  return (
    <div className="flex flex-col gap-3">
      {challenges.map((c) => {
        const pct = Math.min(100, Math.round((c.progress / c.target_count) * 100));
        return (
          <div
            key={c.code}
            className={`rounded-card border px-4 py-3 ${
              c.completed
                ? "border-stamp-teal/40 bg-stamp-teal/10"
                : "border-ink/15 dark:border-paper/15"
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-sm font-medium">
                {c.completed ? "✓ " : ""}
                {c.title}
              </span>
              <span className="font-mono text-xs text-ink/50 dark:text-paper/50">
                {c.progress}/{c.target_count}
              </span>
            </div>
            <p className="text-xs text-ink/60 dark:text-paper/60 mb-2">
              {c.description}
            </p>
            <div className="h-1.5 rounded-full bg-ink/10 dark:bg-paper/10 overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  c.completed ? "bg-stamp-teal" : "bg-stamp-gold"
                }`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
