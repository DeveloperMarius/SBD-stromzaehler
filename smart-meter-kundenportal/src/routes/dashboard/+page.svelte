<script lang="ts">
	import { Card } from 'flowbite-svelte';
	import type { PageData } from './$types';
	import dayjs from 'dayjs';

	export let data: PageData;
	let contracts = data.data.contracts ?? [];
</script>

<svelte:head>
	<title>Übersicht</title>
	<meta name="description" content="Übersicht - Kundendaten" />
	<meta name="robots" content="noindex" />
</svelte:head>

<div class="flex justify-between items-center w-full bg-white px-6 py-2 rounded-md mb-3">
	<h1 class="text-2xl">Übersicht</h1>
</div>

<Card padding="xl" size="lg">
	<div class="flex justify-between items-center mb-4">
		<h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white">Deine Verträge</h5>
		<a
			href="/dashboard/contracts"
			class="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500"
		>
			Alle ansehen
		</a>
	</div>
	{#each contracts as contract, i}
		<div class="flex">
			<p class="mr-2">{i + 1}.</p>
			<div class="flex flex-grow justify-between">
				<p>{contract.name}</p>
				<p>
					{dayjs(contract.startDate).format('DD.MM.YYYY')} - {dayjs(contract.endDate).format(
						'DD.MM.YYYY'
					)}
				</p>
			</div>
		</div>
	{:else}
		<p class="text-gray-600 dark:text-gray-400">Keine Verträge gefunden.</p>
	{/each}
</Card>

<style>
</style>
