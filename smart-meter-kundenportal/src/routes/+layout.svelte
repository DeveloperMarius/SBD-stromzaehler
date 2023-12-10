<script>
	import '../app.css';
	import '@fontsource/roboto';
	import '@fontsource/manrope';

	import { Toaster } from 'svelte-french-toast';
</script>

<Toaster />

<div data-sveltekit-preload-data="false" data-sveltekit-preload-code="false">
	<slot><!-- optional fallback --></slot>
</div>

<style lang="postcss">
	:global(body) {
		min-height: 100vh;
	}
</style>
