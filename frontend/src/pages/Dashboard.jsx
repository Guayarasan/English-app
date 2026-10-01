import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext";
import { fetchDueWords, submitAnswer } from "../services/reviewService";
import { fetchTodayChallenges } from "../services/gamificationService";
import StreakTicket from "../components/StreakTicket";
import ThemeToggle from "../components/ThemeToggle";
import ExerciseRenderer from "../components/exercises/ExerciseRenderer";
import DailyChallenges from "../components/DailyChallenges";
import UnlockToast from "../components/UnlockToast";
import Loading from "../components/Loading";
import EmptyState from "../components/EmptyState";

export default function Dashboard() {
  const { user, logout, setUser } = useAuth();
  const [queue, setQueue] = useState([]);
  const [loadingQueue, setLoadingQueue] = useState(true);
  const [lastFeedback, setLastFeedback] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [toasts, setToasts] = useState([]);
  const [loadError, setLoadError] = useState(false);
  const toastTimers = useRef(new Set());

  useEffect(() => {
    loadQueue();
    fetchTodayChallenges().then(setChallenges).catch(() => {});
    const timers = toastTimers.current;
    return () => timers.forEach(clearTimeout);
  }, []);

  function loadQueue() {
    setLoadingQueue(true);
    setLoadError(false);
    fetchDueWords(15)
      .then((data) => setQueue(data.words))
      .catch(() => setLoadError(true))
      .finally(() => setLoadingQueue(false));
  }

  function pushToasts(newItems) {
    setToasts((prev) => [...prev, ...newItems]);
    newItems.forEach((item) => {
      const timer = setTimeout(() => {
        toastTimers.current.delete(timer);
        dismissToast(item.id);
      }, 4500);
      toastTimers.current.add(timer);
    });
  }

  function dismissToast(id) {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }

  async function handleComplete(result) {
    setUser((prev) => ({
      ...prev,
      xp: result.total_xp,
      level: result.level,
      current_streak: result.current_streak,
    }));
    setLastFeedback({ wasCorrect: result.is_correct, xpEarned: result.xp_earned });
    setQueue((prev) => prev.slice(1));

    if (result.achievements_unlocked.length || result.challenges_completed.length) {
      const items = [
        ...result.achievements_unlocked.map((a) => ({
          id: `ach-${a.code}-${Date.now()}`,
          title: a.title,
          xp_reward: a.xp_reward,
        })),
        ...result.challenges_completed.map((c) => ({
          id: `ch-${c.code}-${Date.now()}`,
          title: c.title,
          xp_reward: c.xp_reward,
        })),
      ];
      pushToasts(items);
      fetchTodayChallenges().then(setChallenges).catch(() => {});
    }
  }

  const currentWord = queue[0];

  return (
    <div className="min-h-dvh px-4 sm:px-6 py-6 sm:py-8 max-w-3xl mx-auto">
      <header className="flex items-start justify-between flex-wrap gap-x-4 gap-y-3 mb-6 sm:mb-10">
        <div>
          <p className="text-sm text-ink/60 dark:text-paper/60">Hola,</p>
          <h1 className="font-display text-2xl break-all">{user?.username}</h1>
        </div>
        <nav aria-label="Navegación principal" className="flex items-center gap-x-4 gap-y-2 flex-wrap">
          <Link
            to="/stats"
            className="text-sm text-ink/60 dark:text-paper/60 hover:text-stamp-teal transition"
          >
            Estadísticas
          </Link>
          <Link
            to="/achievements"
            className="text-sm text-ink/60 dark:text-paper/60 hover:text-stamp-gold transition"
          >
            Logros
          </Link>
          <ThemeToggle />
          <button
            type="button"
            onClick={logout}
            className="text-sm text-ink/60 dark:text-paper/60 hover:text-stamp-coral transition"
          >
            Salir
          </button>
        </nav>
      </header>

      <section
        className="mb-8 sm:mb-10 flex justify-center"
        aria-label={`Racha de ${user?.current_streak ?? 0} días, ${user?.xp ?? 0} puntos de experiencia, nivel ${user?.level ?? 1}`}
      >
        <StreakTicket
          streak={user?.current_streak ?? 0}
          xp={user?.xp ?? 0}
          level={user?.level ?? 1}
        />
      </section>

      <main className="grid md:grid-cols-[minmax(0,1fr)_260px] gap-8">
        <section aria-label="Repaso de hoy">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display text-xl">Repaso de hoy</h2>
            {lastFeedback && (
              <span
                role="status"
                className={`text-sm font-mono ${
                  lastFeedback.wasCorrect ? "text-stamp-teal" : "text-stamp-coral"
                }`}
              >
                +{lastFeedback.xpEarned} xp
              </span>
            )}
          </div>

          {loadingQueue && <Loading label="Preparando tu repaso..." />}

          {!loadingQueue && loadError && (
            <div className="ticket px-6 py-8 text-center">
              <p className="text-sm text-stamp-coral mb-3" role="alert">
                No se pudo cargar tu repaso.
              </p>
              <button
                type="button"
                onClick={loadQueue}
                className="px-4 py-2 min-h-10 rounded-card bg-ink text-paper dark:bg-paper dark:text-ink text-sm font-medium"
              >
                Reintentar
              </button>
            </div>
          )}

          {!loadingQueue && !loadError && queue.length === 0 && (
            <EmptyState
              icon="🛂"
              title="Sellaste tu pasaporte de hoy"
              description="No quedan palabras pendientes por ahora. Vuelve más tarde."
            />
          )}

          {!loadingQueue && currentWord && (
            <div className="flex flex-col items-center gap-6">
              <ExerciseRenderer
                key={currentWord.id}
                word={currentWord}
                submitAnswer={submitAnswer}
                onComplete={handleComplete}
              />
              <span className="font-mono text-sm text-ink/50 dark:text-paper/50">
                {queue.length} pendiente{queue.length === 1 ? "" : "s"}
              </span>
            </div>
          )}
        </section>

        <aside aria-label="Desafíos de hoy">
          <h2 className="font-display text-xl mb-4">Desafíos de hoy</h2>
          <DailyChallenges challenges={challenges} />
        </aside>
      </main>

      <UnlockToast items={toasts} onDismiss={dismissToast} />
    </div>
  );
}
