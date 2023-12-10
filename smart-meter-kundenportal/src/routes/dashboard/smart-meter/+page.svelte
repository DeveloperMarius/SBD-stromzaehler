<script lang="ts">
	import { Card, Chart } from 'flowbite-svelte';
	import dayjs from 'dayjs';
	import { page } from '$app/stores';
	import type { PageData } from './$types';
	import { onMount } from 'svelte';
	import type { Reading } from '$lib/reading';

	export let data: PageData;

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
		let highestReadingDate = 2123;

		powermeterReadings.forEach((powermeterReading) => {
			if (powermeterReading.value > highestReading) {
				highestReading = powermeterReading.value;
				highestReadingDate = powermeterReading.timestamp;
			}
		});

		return { highestReading, highestReadingDate };
	}

	/** Returns only values from today*/
	function getReadingsForChart(powermeterReadings: Reading[]) {
		let values: number[] = [];
		let dates: string[] = [];
		powermeterReadings.sort((a, b) => {
			return a.timestamp - b.timestamp;
		});

		powermeterReadings.filter((powermeterReading) => {
			return (
				dayjs(powermeterReading.timestamp).format('DD.MM.YYYY') == dayjs().format('DD.MM.YYYY')
			);
		});

		powermeterReadings.forEach((powermeterReading) => {
			values.push(powermeterReading.value);
			dates.push(dayjs(powermeterReading.timestamp).format('HH:mm'));
		});

		return {
			x: dates,
			y: values
		};
	}

	const options = (x: string[], y: number[]): ApexCharts.ApexOptions => {
		return {
			chart: {
				height: '200px',
				type: 'area',
				fontFamily: 'Inter, sans-serif',
				dropShadow: {
					enabled: false
				},
				toolbar: {
					show: false
				}
			},
			tooltip: {
				enabled: true,
				x: {
					show: false
				}
			},
			fill: {
				type: 'gradient',
				gradient: {
					opacityFrom: 0.55,
					opacityTo: 0,
					shade: '#1C64F2',
					gradientToColors: ['#1C64F2']
				}
			},
			dataLabels: {
				enabled: false
			},
			stroke: {
				width: 6
			},
			grid: {
				show: false,
				strokeDashArray: 4,
				padding: {
					left: 2,
					right: 2,
					top: 0
				}
			},
			series: [
				{
					name: 'New users',
					data: y,
					color: '#1A56DB'
				}
			],
			xaxis: {
				categories: x,
				labels: {
					show: true
				},
				axisBorder: {
					show: false
				},
				axisTicks: {
					show: false
				}
			},
			yaxis: {
				show: false
			}
		};
	};
</script>

<svelte:head>
	<title>Stromzähler</title>
</svelte:head>

<div class="flex justify-between items-center w-full bg-white px-6 py-2 rounded-md mb-3 shadow-md">
	<h1 class="text-2xl">Ihre Stromzähler</h1>
</div>

{#if contracts && powermeterReadings}
	{#key contracts}
		{#each contracts as contract}
			{#key powermeterReadings}
				{#each powermeterReadings as powermeterReading}
					{#if powermeterReading.contract_id == contract.id}
						<Card padding="xl" class="max-w-full">
							<div class="flex justify-between items-center mb-4">
								<h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white">
									{contract.name}
									({powermeterReading.powermeter_id})
								</h5>
								<p>
									({dayjs(contract.startDate).format('DD.MM.YYYY')} - {dayjs(
										contract.endDate
									).format('DD.MM.YYYY')})
								</p>
							</div>
							{#if powermeterReading.readings}
								<Chart
									options={options(
										getReadingsForChart(powermeterReading.readings).x,
										getReadingsForChart(powermeterReading.readings).y
									)}
								/>
							{/if}
							<div class="flex justify-between items-center w-full mt-4 rounded-md">
								<div class="flex flex-col">
									<p class="text-md">Aktueller Zählerstand</p>
									<p class="text-lg">
										{getHighestReading(powermeterReading.readings).highestReading} kWh
									</p>
								</div>
								<div class="flex flex-col">
									<p class="text-md">Zählerstand vom</p>
									<p class="text-lg">
										{dayjs(getHighestReading(powermeterReading.readings).highestReadingDate).format(
											'DD.MM.YYYY [um] HH:mm [Uhr]'
										)}
									</p>
								</div>
							</div>
						</Card>
					{/if}
				{/each}
			{/key}
		{/each}
	{/key}
{:else}
	<p>Verträge werden geladen</p>
{/if}
