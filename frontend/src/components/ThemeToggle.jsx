import { useTheme } from "../features/theme/ThemeContext";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label="Cambiar tema"
      className="w-10 h-10 rounded-full border border-ink/20 dark:border-paper/20 flex items-center justify-center hover:bg-ink/5 dark:hover:bg-paper/10 transition"
    >
      <span aria-hidden="true">{theme === "light" ? "🌙" : "☀️"}</span>
    </button>
  );
}
