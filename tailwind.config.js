/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.html", "**/static/**/*.js"],
  theme: {
    extend: {
      backgroundImage: {
        "bg-login": "url('/mindtechcare/static/images/bg.png')",
      },
      colors: {
        primary: "#10b981",
      },
    },
  },
  plugins: [],
};
