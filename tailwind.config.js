/** @type {import('tailwindcss').Config} */
function clay(shade) {
  return `rgb(var(--clay-${shade}) / <alpha-value>)`;
}
function stone(shade) {
  return `rgb(var(--stone-${shade}) / <alpha-value>)`;
}

const clayRamp = {
  50: clay(50), 100: clay(100), 200: clay(200), 300: clay(300), 400: clay(400),
  500: clay(500), 600: clay(600), 700: clay(700), 800: clay(800), 900: clay(900),
};
const stoneRamp = {
  50: stone(50), 100: stone(100), 200: stone(200), 300: stone(300), 400: stone(400),
  500: stone(500), 600: stone(600), 700: stone(700), 800: stone(800), 900: stone(900), 950: stone(950),
};

module.exports = {
  content: ['./**/*.html'],
  theme: {
    extend: {
      colors: {
        indigo: clayRamp,
        purple: clayRamp,
        clay: clayRamp,
        gray: stoneRamp,
      },
      fontFamily: {
        sans: ['Hanken Grotesk', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Instrument Serif', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: {
        lg: '0.625rem',
        xl: '0.625rem',
        '2xl': '0.625rem',
      },
      letterSpacing: {
        tightest: '-0.03em',
      },
    },
  },
};
