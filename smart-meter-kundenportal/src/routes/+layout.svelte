<script>
	import '../app.css';
	import '@fontsource/roboto';
	import '@fontsource/manrope';
</script>

<slot><!-- optional fallback --></slot>

<style lang="postcss">
	:global(body) {
		min-height: 100vh;
	}
</style>
