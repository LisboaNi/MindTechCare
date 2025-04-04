/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./mindtechcare/templates/**/*.html", "./mindtechcare/static/**/*.js"],
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
