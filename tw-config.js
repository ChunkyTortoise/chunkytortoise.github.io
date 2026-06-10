/*
 * Central Tailwind (Play CDN, v3) theme override - single source of truth for
 * the site palette + type. Loaded once per page right after the CDN script,
 * before Tailwind scans the DOM. Change colors/fonts/radius HERE, not per page.
 *
 * Tokens are stored as space-separated RGB channels in style.css :root and
 * wrapped with the <alpha-value> placeholder so Tailwind opacity modifiers
 * (e.g. bg-indigo-600/20) and gradient stops keep working. A bare var() with a
 * hex value silently breaks those - do not change this shape.
 *
 * Design direction (matches the ai-dashboard warm-editorial identity):
 *   accent  = clay / terracotta (#CC785C), the anti "AI purple"
 *   neutral = warm stone ramp (no pure #fff / #000)
 *   display = Instrument Serif (titles only)   body = Hanken Grotesk   mono = JetBrains Mono
 *
 * The legacy palette names `indigo` and `purple` are remapped to the same clay
 * ramp so existing utility classes (and the hero gradient) recolor at once
 * without touching 1100+ class strings.
 */
function clay(shade) { return `rgb(var(--clay-${shade}) / <alpha-value>)`; }
function stone(shade) { return `rgb(var(--stone-${shade}) / <alpha-value>)`; }

const clayRamp = {
  50: clay(50), 100: clay(100), 200: clay(200), 300: clay(300), 400: clay(400),
  500: clay(500), 600: clay(600), 700: clay(700), 800: clay(800), 900: clay(900),
};
const stoneRamp = {
  50: stone(50), 100: stone(100), 200: stone(200), 300: stone(300), 400: stone(400),
  500: stone(500), 600: stone(600), 700: stone(700), 800: stone(800), 900: stone(900), 950: stone(950),
};

tailwind.config = {
  theme: {
    extend: {
      colors: {
        // remap the slop names to clay; new semantic name `clay` also available
        indigo: clayRamp,
        purple: clayRamp,
        clay: clayRamp,
        // warm the neutrals: gray -> warm stone
        gray: stoneRamp,
      },
      fontFamily: {
        sans: ['Hanken Grotesk', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Instrument Serif', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      // commit one corner stance: collapse the lg/xl sprawl to a single 10px token
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
