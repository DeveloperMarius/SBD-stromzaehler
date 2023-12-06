<script>
	import '../app.css';
	import '@fontsource/roboto';
	import '@fontsource/manrope';

	import { Toaster } from 'svelte-french-toast';
</script>

<Toaster />

<slot><!-- optional fallback --></slot>

<style lang="postcss">
	:global(body) {
		min-height: 100vh;
	}
</style>
