/** @type {import('tailwindcss').Config} */
module.exports = {
content: ["../../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        emerald: {
          950: '#064e3b',
        },
        zinc: {
          300: '#a1a1aa',
        }
      },
    },
  },
  plugins: [],
}

