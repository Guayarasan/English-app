/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Modo oscuro = "tinta noche" / modo claro = "papel"
        ink: {
          DEFAULT: "#161C2C",
          light: "#232B40",
        },
        paper: {
          DEFAULT: "#F4EFE3",
          dim: "#E8E1D0",
        },
        stamp: {
          gold: "#C9A227",
          coral: "#E85D4C",
          teal: "#2F6F62",
        },
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        sans: ["Inter", "sans-serif"],
        mono: ["Space Mono", "monospace"],
      },
      borderRadius: {
        card: "14px",
      },
    },
  },
  plugins: [],
};
