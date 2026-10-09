/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // ── CMIT Solutions official palette (Brand Guide v2.1) ──
        // Primary
        navy: '#002F44', // Dark Navy Blue — primary brand blue / dark bg
        red: '#EF3F37', // Red — logo accent / primary highlight
        // Secondary
        'navy-deep': '#001B28', // deep background variation
        orange: '#EF9637',
        teal: '#25B17E', // green/teal — specific purposes only
        'cmit-gray': '#D0DADF', // interactive / hover
        'light-blue': '#B0D3E4', // backgrounds
        // New approved (2025)
        'bright-blue': '#3291DB', // emphasis, CTAs, backgrounds
        'royal-purple': '#7035FF', // high-impact headers/highlights

        // ── Semantic aliases used across components ──
        bg: '#002F44', // navy
        surface: '#001B28', // navy-deep
        fg: '#ffffff',
        muted: '#B0D3E4', // light blue reads as muted on navy
        accent: '#EF3F37', // red
        accent2: '#3291DB', // bright blue
      },
      fontFamily: {
        // Avenir is the CMIT primary typeface; Arial is the approved fallback.
        sans: ['Avenir Next', 'Avenir', 'Arial', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        content: '72rem',
      },
      backgroundImage: {
        // Approved linear gradients (radial is NOT approved by the brand guide)
        'cmit-blue-purple': 'linear-gradient(135deg, #3291DB, #7035FF)',
        'cmit-navy-blue': 'linear-gradient(135deg, #002F44, #3291DB)',
        'cmit-red-blue': 'linear-gradient(135deg, #EF3F37, #3291DB)',
        'cmit-navy-green': 'linear-gradient(135deg, #002F44, #25B17E)',
      },
    },
  },
  plugins: [],
}
