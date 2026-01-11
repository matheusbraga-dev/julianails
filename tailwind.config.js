module.exports = {
  content: [
    './**/templates/**/*.html',
    './**/forms.py',
  ],
    theme: {
        extend: {
            colors: {
                lilac: {
                    50: '#fdf4ff',
                    100: '#fae8ff',
                    200: '#f5d0fe',
                    300: '#e8bdfc',
                    400: '#c58af9',
                    500: '#aa70c2',
                    600: '#8a4fb7',
                    700: '#4c00d6',
                    800: '#3c00a8',
                    900: '#1a0033',
                    950: '#100020',
                },
                gold: {
                    100: '#f9f1d8',
                    300: '#e8d28a',
                    500: '#d4af37',
                }
            },
            fontFamily: {
                'display': ['"Playfair Display"', 'serif'],
                'body': ['"Lato"', 'sans-serif'],
                'script': ['"Damion"', 'cursive'],
            },
            backgroundImage: {
                'soft-glow': 'linear-gradient(135deg, #fdf4ff 0%, #fae8ff 50%, #f3e5f5 100%)',
                'pattern-dots': 'radial-gradient(circle, #e8bdfc 1px, transparent 1px)',
            },
            backgroundSize: {
                'pattern-dots': '20px 20px',
            },
            animation: {
                'fade-in-up': 'fadeInUp 1s ease-out forwards',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            }
        }
    },
  plugins: [],
}