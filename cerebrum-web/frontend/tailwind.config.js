/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary (dark grays - Obsidian style)
        primary: {
          900: '#1a1a1a',  // Deep black (bg)
          800: '#2a2a2a',  // Card bg
          700: '#3a3a3a',  // Hover bg
          600: '#4a4a4a',  // Border
          500: '#6a6a6a',  // Muted text
          400: '#8a8a8a',  // Secondary text
          300: '#aaaaaa',  // Tertiary text
          200: '#d1d1d1',  // Primary text
          100: '#f5f5f5',  // Bright white
        },
        // Accent (Obsidian purple + others)
        accent: {
          purple: '#9b87f5',   // Primary actions
          blue: '#5e8cff',     // Links
          green: '#4ade80',    // Success
          red: '#f87171',      // Error
          yellow: '#fbbf24',   // Warning
          orange: '#fb923c',   // Processing
        }
      },
      fontFamily: {
        display: ['Montserrat', 'system-ui', 'sans-serif'],
        body: ['Poppins', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'monospace'],
      },
      borderRadius: {
        'apple-sm': '6px',
        'apple-md': '12px',
        'apple-lg': '16px',
        'apple-xl': '24px',
      },
      boxShadow: {
        'glow-purple': '0 0 20px rgba(155, 135, 245, 0.3)',
      }
    },
  },
  plugins: [],
}
