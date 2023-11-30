/** @type {import('tailwindcss').Config} */
export default {
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'
	],

	plugins: [require('flowbite/plugin')],

	darkMode: 'class',

	theme: {
		fontFamily: {
			sans: ['Roboto', 'sans-serif'],
			serif: ['Manrope', 'serif']
		},

		extend: {
			colors: {
				// flowbite-svelte
				primary: {
					50: '#FFF5F2',
					100: '#FFF1EE',
					200: '#FFE4DE',
					300: '#FFD5CC',
					400: '#FFBCAd',
					500: '#FE795D',
					600: '#56e08c',
					700: '#189982',
					800: '#0497a1',
					900: '#0A5580'
				}
			},
			backgroundImage: {
				'electr-bg': "url('/background.jpg')"
			}
		}
	}
};
