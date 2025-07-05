/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //tailwind css works on root level templates directory
    "./**/templates/**/*.html" //tailwind css works on app level templates directory
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: false, // disable default themes
  },
}

