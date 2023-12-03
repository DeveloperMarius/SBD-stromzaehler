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
					50: '#DCF1C8',
					100: '#FFF1EE',
					200: '#EEE881', //gelb
					300: '#98D789', // noch hellgrün
					400: '#ACEF92', //hellgrün
					500: '#018590', //grünblau
					600: '#0A84B0', // wenig heller blau
					700: '#0B6988', //navi 
					800: '#59B78C', // grün
					900: '#1E6952' //navi
				},
				lighty: {
					50: '#DCF1C8',
					100: '#62C8E4', //skyblue
					200: '#DCF1C8', 
					300: '#DCF1C8', 
					400: '#DCF1C8', 
					500: '#DCF1C8', 
					600: '#DCF1C8', 
					700: '#DCF1C8', 
					800: '#DCF1C8', 
					900: '#DCF1C8' 
				}
			},
			backgroundImage: {
				'electr-bg': "url('/background.jpg')"
			}
		}
	}
};
