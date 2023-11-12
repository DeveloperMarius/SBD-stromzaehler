<script>
	import '../app.css';
</script>

<div id="bg-img">
	<slot><!-- optional fallback --></slot>
</div>

<style lang="postcss">	
	#bg-img {
		background: url(/background.png) no-repeat center center fixed;
	}
</style>
