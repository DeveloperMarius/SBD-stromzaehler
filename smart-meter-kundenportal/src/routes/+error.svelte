<script>
	import { Section, Page404 } from 'flowbite-svelte-blocks';
	import { page } from '$app/stores';
</script>

<div class="flex justify-center items-center h-screen">
	<Section name="page404">
		<Page404>
			<svelte:fragment slot="h1">{$page.status}</svelte:fragment>
			<svelte:fragment slot="paragraph">
				<p class="mb-4 text-3xl tracking-tight font-bold text-gray-900 md:text-4xl dark:text-white">
					{$page?.error?.message ?? 'Page not found'}
				</p>
			</svelte:fragment>
		</Page404>
	</Section>
</div>
