import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchAchievements } from "../services/gamificationService";
import Loading from "../components/Loading";

/**
 * Página de logros como "álbum de sellos" del pasaporte: los
 * desbloqueados se ven a color con el sello dorado, los pendientes en
 * gris tenue — refuerza la metáfora de viaje sin repetir el ticket.
 */
export default function Achievements() {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAchievements()
      .then(setAchievements)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-dvh px-4 sm:px-6 py-6 sm:py-8 max-w-3xl mx-auto">
      <header className="mb-8">
        <Link
          to="/dashboard"
          className="text-sm text-ink/60 dark:text-paper/60 hover:text-stamp-teal transition"
        >
          ← Volver
        </Link>
        <h1 className="font-display text-2xl mt-1">Álbum de sellos</h1>
      </header>

      {loading ? (
        <Loading label="Cargando logros..." />
      ) : (
        <main className="grid sm:grid-cols-2 gap-4" aria-label="Catálogo de logros">
          {achievements.map((a) => (
            <div
              key={a.code}
              className={`rounded-card border p-4 flex items-start gap-3 ${
                a.unlocked
                  ? "border-stamp-gold/50 bg-stamp-gold/10"
                  : "border-ink/10 dark:border-paper/10 opacity-50"
              }`}
            >
              <span className="text-2xl" aria-hidden="true">
                {a.unlocked ? "🏅" : "🔒"}
              </span>
              <div>
                <p className="font-medium">
                  {a.title}
                  <span className="sr-only">
                    {a.unlocked ? " (desbloqueado)" : " (bloqueado)"}
                  </span>
                </p>
                <p className="text-sm text-ink/60 dark:text-paper/60 mb-1">
                  {a.description}
                </p>
                <span className="font-mono text-xs text-stamp-gold">
                  +{a.xp_reward} xp
                </span>
              </div>
            </div>
          ))}
        </main>
      )}
    </div>
  );
}
