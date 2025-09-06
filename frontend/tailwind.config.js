/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2563eb",    // Blue – academic accent
        secondary: "#16a34a",  // Green – success/highlight
        accent: "#fbbf24",     // Yellow – highlight for alerts/CTAs
        neutral: "#f5f5f5",    // Light background for sections
        dark: "#1e293b",       // Dark navy for headers
      },
      fontFamily: {
        sans: ["Poppins", "sans-serif"],
        heading: ["Merriweather", "serif"], // For headings
      },
      borderRadius: {
        card: "1rem", // Rounded edges for cards
      },
      boxShadow: {
        soft: "0 4px 12px rgba(0, 0, 0, 0.1)", // Soft shadow for cards
      },
    },
  },
  plugins: [],
}
