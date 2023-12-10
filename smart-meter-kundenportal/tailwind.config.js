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
					50: '#2fffa2',
					100: '#16ff96',
					200: '#00fb8a', //gelb
					300: '#00e17c', // noch hellgrün
					400: '#00c76d', //hellgrün
					500: '#00ad5f', //grünblau
					600: '#009351', // wenig heller blau
					700: '#007943', //navi
					800: '#005f34', // grün
					900: '#004526' //navi
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
