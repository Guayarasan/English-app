import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import {
  fetchStatsSummary,
  fetchStatsHistory,
  fetchCategoryStats,
  fetchHardestWords,
} from "../services/statsService";
import Loading from "../components/Loading";

const COLORS = { gold: "#C9A227", coral: "#E85D4C", teal: "#2F6F62" };

function SummaryCard({ label, value, accent }) {
  return (
    <div className="ticket px-3 sm:px-5 py-4 flex flex-col items-center text-center">
      <span className="font-mono text-2xl font-bold" style={{ color: accent }}>
        {value}
      </span>
      <span className="text-xs uppercase tracking-wide text-ink/60 dark:text-paper/60 mt-1">
        {label}
      </span>
    </div>
  );
}

export default function Stats() {
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [categories, setCategories] = useState([]);
  const [hardestWords, setHardestWords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchStatsSummary(),
      fetchStatsHistory(30),
      fetchCategoryStats(),
      fetchHardestWords(8),
    ])
      .then(([s, h, c, w]) => {
        setSummary(s);
        setHistory(h);
        setCategories(c);
        setHardestWords(w);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-dvh flex items-center justify-center px-6">
        <Loading label="Cargando estadísticas..." />
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="min-h-dvh flex flex-col items-center justify-center gap-4 px-6 text-center">
        <p role="alert" className="text-sm text-stamp-coral">
          No se pudieron cargar las estadísticas.
        </p>
        <Link to="/dashboard" className="text-sm text-stamp-teal font-medium">
          ← Volver
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-dvh px-4 sm:px-6 py-6 sm:py-8 max-w-3xl mx-auto">
      <header className="mb-8">
        <Link
          to="/dashboard"
          className="text-sm text-ink/60 dark:text-paper/60 hover:text-stamp-teal transition"
        >
          ← Volver
        </Link>
        <h1 className="font-display text-2xl mt-1">Bitácora de viaje</h1>
      </header>

      <main>

      <section className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-10">
        <SummaryCard label="Precisión" value={`${summary.accuracy}%`} accent={COLORS.teal} />
        <SummaryCard label="Intentos" value={summary.total_attempts} accent={COLORS.gold} />
        <SummaryCard label="Aprendidas" value={summary.words_learned} accent={COLORS.gold} />
        <SummaryCard label="En progreso" value={summary.words_in_progress} accent={COLORS.coral} />
      </section>

      <section className="mb-10">
        <h2 className="font-display text-xl mb-4">Últimos 30 días</h2>
        <div className="ticket px-2 sm:px-4 py-4 h-56 sm:h-64">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={history}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 10 }}
                tickFormatter={(d) => d.slice(5)}
                interval="preserveStartEnd" minTickGap={24}
              />
              <YAxis yAxisId="left" tick={{ fontSize: 10 }} />
              <YAxis yAxisId="right" orientation="right" domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Tooltip
                contentStyle={{ fontSize: 12, borderRadius: 10 }}
                labelFormatter={(d) => `Fecha: ${d}`}
              />
              <Bar yAxisId="left" dataKey="attempts" fill={COLORS.gold} radius={[4, 4, 0, 0]} name="Intentos" />
              <Line
                yAxisId="right"
                dataKey="accuracy"
                stroke={COLORS.teal}
                strokeWidth={2}
                dot={false}
                name="Precisión %"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </section>

      {categories.length > 0 && (
        <section className="mb-10">
          <h2 className="font-display text-xl mb-4">Precisión por categoría</h2>
          <div className="flex flex-col gap-3">
            {categories.map((c) => (
              <div key={c.category} className="flex items-center gap-3">
                <span className="w-20 sm:w-24 shrink-0 truncate text-sm capitalize text-ink/70 dark:text-paper/70" title={c.category}>
                  {c.category}
                </span>
                <div className="flex-1 h-3 rounded-full bg-ink/10 dark:bg-paper/10 overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{ width: `${c.accuracy}%`, backgroundColor: COLORS.teal }}
                  />
                </div>
                <span className="font-mono text-xs w-12 shrink-0 text-right">{c.accuracy}%</span>
              </div>
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="font-display text-xl mb-4">Palabras más difíciles</h2>
        {hardestWords.length === 0 ? (
          <p className="text-ink/60 dark:text-paper/60 text-sm">
            Todavía no tienes suficiente historial para esto.
          </p>
        ) : (
          <div className="grid sm:grid-cols-2 gap-3">
            {hardestWords.map((w) => (
              <div
                key={w.text_en}
                className="rounded-card border border-stamp-coral/30 bg-stamp-coral/5 px-4 py-3"
              >
                <p className="font-display text-lg">{w.text_en}</p>
                <p className="text-sm text-ink/60 dark:text-paper/60 mb-1">{w.text_es}</p>
                <span className="font-mono text-xs text-stamp-coral">
                  {w.fail_count} fallos · {w.success_count} aciertos
                </span>
              </div>
            ))}
          </div>
        )}
      </section>
      </main>
    </div>
  );
}
