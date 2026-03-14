/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#f5f1e8',
        primary: '#8b7355',
        accent: '#c6a969',
        text: '#3a3327',
        sidebar: '#e8e2d4',
        card: '#faf7f2'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
