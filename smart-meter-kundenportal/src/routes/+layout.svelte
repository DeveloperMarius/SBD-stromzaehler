<script>
	import '../app.css';
</script>

<div>
	<slot><!-- optional fallback --></slot>
</div>

<style lang="postcss">
	div {
		@apply bg-primary-200 min-h-screen;
	}
</style>
