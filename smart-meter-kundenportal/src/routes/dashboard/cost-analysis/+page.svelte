<script lang="ts">
	import dayjs from 'dayjs';
	import { page } from '$app/stores';
	import type { PageData } from './$types';
	import { onMount } from 'svelte';
	import type { PowermeterReading, Reading } from '$lib/reading';
	import {
		Card,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';

	export let data: PageData;

	const price: number = 29.44;

	let contracts = data.data.contracts;
	let powermeterReadings = data.data.powermeterReadings;

	onMount(async () => {
		page.subscribe(async (pageData) => {
			if (pageData.status === 200) {
				contracts = data.data.contracts;
				powermeterReadings = data.data.powermeterReadings;
			}
		});
	});

	function getHighestReading(powermeterReadings: Reading[]) {
		let highestReading = 0;

		powermeterReadings.forEach((powermeterReading) => {
			if (powermeterReading.value > highestReading) {
				highestReading = powermeterReading.value;
			}
		});

		return highestReading;
	}

	function getLowestReading(powermeterReadings: Reading[]) {
		let lowestReading = 0;

		powermeterReadings.forEach((powermeterReading) => {
			if (powermeterReading.value < lowestReading) {
				lowestReading = powermeterReading.value;
			}
		});

		return lowestReading;
	}

	function lastThirtyDays(powermeterReadings: PowermeterReading[]) {
		let lastThirtyDays: {
			contract_id: string;
			powermeter_id: string;
			readings: Reading[];
		}[] = [];

		powermeterReadings.forEach((powermeterReading) => {
			lastThirtyDays.push({
				powermeter_id: powermeterReading.powermeter_id,
				contract_id: powermeterReading.contract_id,
				readings: powermeterReading.readings.filter((reading) =>
					dayjs(reading.timestamp).isAfter(dayjs().subtract(30, 'day'))
				)
			});
		});

		return lastThirtyDays;
	}

	function getValuesForEachDay(powermeterReadings: Reading[]) {
		let values: number[] = [];
		let dates: string[] = [];
		powermeterReadings.sort((a, b) => {
			return a.timestamp - b.timestamp;
		});

		let days: Set<string> = new Set();

		powermeterReadings.forEach((powermeterReading) => {
			days.add(dayjs(powermeterReading.timestamp).format('DD.MM.YYYY'));
		});

		let dayValues: {
			day: string;
			lowest_value: number;
			highest_value: number;
		}[] = [];

		days.forEach((day) => {
			const dayReadings = powermeterReadings.filter((powermeterReading) => {
				return dayjs(powermeterReading.timestamp).format('DD.MM.YYYY') == day;
			});

			dayValues.push({
				day,
				lowest_value: getLowestReading(dayReadings),
				highest_value: getHighestReading(dayReadings)
			});
		});

		return dayValues;
	}

	function calculatePrice(reading: { day: string; lowest_value: number; highest_value: number }) {
		const kwhPrice = ((reading.highest_value - reading.lowest_value) * price) / 100;

		return Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(kwhPrice);
	}

	function totalPrice(powermeterReadings: Reading[]) {
		let totalPrice = 0;

		getValuesForEachDay(powermeterReadings).forEach((reading) => {
			totalPrice += ((reading.highest_value - reading.lowest_value) * price) / 100;
		});

		return Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(totalPrice);
	}
</script>

<svelte:head>
	<title>Preisübersicht</title>
</svelte:head>

<div class="flex justify-between items-center w-full bg-white px-6 py-2 rounded-md mb-3 shadow-md">
	<h1 class="text-2xl">Ihre Preisübersicht</h1>
</div>

{#if contracts && powermeterReadings}
	{#key contracts}
		{#each contracts as contract}
			<Card class="w-full max-w-full">
				<h1 class="mb-4 ml-2 text-lg font-serif">{contract.name} (letzte 30 Tage)</h1>
				<Table shadow>
					<TableHead class="bg-slate-200">
						<TableHeadCell>Datum</TableHeadCell>
						<TableHeadCell>Zählerstand (min)</TableHeadCell>
						<TableHeadCell>Zählerstand (max)</TableHeadCell>
						<TableHeadCell>Gesamt</TableHeadCell>
					</TableHead>
					<TableBody tableBodyClass="divide-y">
						{#key powermeterReadings}
							{#each lastThirtyDays(powermeterReadings) as powermeterReading}
								{#if powermeterReading.contract_id == contract.id}
									{#each getValuesForEachDay(powermeterReading.readings) as reading}
										<TableBodyRow>
											<TableBodyCell>{reading.day}</TableBodyCell>
											<TableBodyCell>{reading.lowest_value} kwH</TableBodyCell>
											<TableBodyCell>{reading.highest_value} kwH</TableBodyCell>
											<TableBodyCell>
												{calculatePrice(reading)}
											</TableBodyCell>
										</TableBodyRow>
									{/each}
									<TableBodyRow class="bg-slate-200">
										<TableBodyCell>Gesamt</TableBodyCell>
										<TableBodyCell />
										<TableBodyCell />
										<TableBodyCell>{totalPrice(powermeterReading.readings)}</TableBodyCell>
									</TableBodyRow>
								{/if}
							{/each}
						{/key}
					</TableBody>
				</Table>
			</Card>
		{/each}
	{/key}
{:else}
	<p>Verträge werden geladen</p>
{/if}
