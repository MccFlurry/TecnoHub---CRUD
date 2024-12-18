module.exports = {
  purge: ['./templates/**/*.html', './static/js/**/*.js'],
  darkMode: false,
  theme: {

    extend: {},

  },

  variants: {

    extend: {},

  },

  plugins: [

    require('@tailwindcss/forms'),

    require('@tailwindcss/typography'),

    require('@tailwindcss/aspect-ratio'),

  ],
}
