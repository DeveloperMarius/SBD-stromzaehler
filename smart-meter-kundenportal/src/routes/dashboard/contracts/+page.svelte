<script lang="ts">
	import { Button, Label, Modal, Input, Checkbox, Card } from 'flowbite-svelte';
	import type { PageData } from './$types';
	import { enhance } from '$app/forms';
	import dayjs from 'dayjs';
	import { page } from '$app/stores';
	import { TrashBinOutline, EditOutline } from 'flowbite-svelte-icons';
	import type { Contract } from '@prisma/client';

	let defaultModal = false;
	let editModal = false;
	let editContract: Partial<Contract> = {};
	let deleteModal = false;

	export let data: PageData;

	let user = data.data.user;
	let contracts = data.data.contracts;

	page.subscribe((pageData) => {
		if (pageData.status === 200) {
			defaultModal = false;
			deleteModal = false;
		}

		user = data.data.user;
		contracts = data.data.contracts;
	});
</script>

<svelte:head>
	<title>Vertragsübersicht</title>
</svelte:head>

<div class="flex justify-between items-center w-full bg-white px-6 py-2 rounded-md mb-3 shadow-md">
	<h1 class="text-2xl">Ihre Verträge</h1>
	<Button on:click={() => (defaultModal = true)}>Vertrag abschließen</Button>
</div>

<div class="grid xl:grid-cols-2 gap-2">
	{#each contracts as contract, i}
		<Card padding="xl" class="max-w-full">
			<div class="flex justify-between items-center mb-4">
				<h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white">
					{contract.name}
				</h5>
				<p>
					({dayjs(contract.startDate).format('DD.MM.YYYY')} - {dayjs(contract.endDate).format(
						'DD.MM.YYYY'
					)})
				</p>
			</div>
			<div class="grid grid-cols-2">
				<p class="text-gray-600 dark:text-gray-400">Vorname: {user.vorname}</p>
				<p class="text-gray-600 dark:text-gray-400">Nachname: {user.nachname}</p>
			</div>
			<hr class="my-2" />
			<div class="grid grid-cols-2">
				<p class="text-gray-600 dark:text-gray-400">Straße: {contract.strasse}</p>
				<p class="text-gray-600 dark:text-gray-400">Hausnummer: {contract.hausnr}</p>
				<p class="text-gray-600 dark:text-gray-400">Ort: {contract.ort}</p>
				<p class="text-gray-600 dark:text-gray-400">Ort: {contract.plz}</p>
			</div>
			<hr class="my-2" />
			<div class="grid grid-cols-2">
				<p class="text-gray-600 dark:text-gray-400">IBAN: *********{contract.iban.substring(10)}</p>
				<p class="text-gray-600 dark:text-gray-400">BIC: {contract.blz}</p>
			</div>
			<div class="flex justify-end mt-4 gap-2">
				<Button
					on:click={() => {
						editModal = true;
						editContract = contract;
					}}
					class="flex items-center justify-center gap-2  bg-blue-400 hover:bg-blue-500"
				>
					<EditOutline size="sm" />
					<p>Bankverbindung ändern</p>
				</Button>
				<Button
					on:click={() => (deleteModal = true)}
					class="flex items-center justify-center gap-2  bg-red-700 hover:bg-red-800"
				>
					<TrashBinOutline size="sm" />
					<p>Vertrag kündigen</p>
				</Button>
			</div>
			<Modal title="Vertrag abschließen" bind:open={deleteModal} outsideclose>
				<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
					Wenn Sie Ihren Vertrag kündigen, werden Sie keine weiteren Rechnungen erhalten und Ihr
					Strom wird nach Ablauf der Vertragslaufzeit abgeschaltet.
				</p>

				<form method="POST" action="?/delete_contract" use:enhance>
					<input type="hidden" name="contract_id" value={contract.id} />
					<Button type="submit" class="w-full mt-1 bg-red-700 hover:bg-red-800">
						Vertrag kündigen
					</Button>
				</form>
			</Modal>
		</Card>
	{:else}
		<p class="text-gray-600 dark:text-gray-400">Keine Verträge gefunden.</p>
	{/each}
</div>

<Modal title="Vertrag abschließen" bind:open={defaultModal} outsideclose>
	<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
		Bitte füllen Sie das folgende Formular aus, um Ihren Stromvertrag abzuschließen und von unseren
		Energieangeboten zu profitieren.
	</p>

	<form method="POST" action="?/create_contract" use:enhance>
		<input type="hidden" name="user_id" value={user.id} />
		<div class="grid gap-4 sm:grid-cols-2 sm:gap-6">
			<Label class="space-y-2">
				<span>Straße</span>
				<Input
					type="text"
					name="strasse"
					placeholder="Schlossallee"
					required
					value={user.strasse}
				/>
			</Label>
			<Label class="space-y-2">
				<span>Hausnummer</span>
				<Input type="text" name="hausnr" placeholder="400" required value={user.hausnr} />
			</Label>
			<Label class="space-y-2">
				<span>Ort</span>
				<Input type="text" name="ort" placeholder="Musterstadt" required value={user.ort} />
			</Label>
			<Label class="space-y-2">
				<span>Postleitzahl</span>
				<Input type="text" name="plz" placeholder="12345" required value={user.plz} />
			</Label>
		</div>
		<hr class="my-4" />
		<div class="grid gap-4 sm:grid-cols-2 sm:gap-6 mb-4">
			<Label class="space-y-2">
				<span>IBAN</span>
				<Input type="text" name="iban" placeholder="DE12378213781237" required />
			</Label>
			<Label class="space-y-2">
				<span>BIC</span>
				<Input type="text" name="blz" placeholder="COM81932XXX" required />
			</Label>
		</div>
		<div class="flex items-start mb-2">
			<Checkbox>
				Ich stimme dem <a
					class="font-medium text-primary-600 hover:underline dark:text-primary-500 mx-1"
					href="/"
				>
					SEPA Lastschriftmandat
				</a>
				zu
			</Checkbox>
		</div>
		<hr class="my-4" />

		<div class="flex items-start mb-4">
			<Checkbox>
				Ich akzeptiere die <a
					class="font-medium text-primary-600 hover:underline dark:text-primary-500 ml-1"
					href="/"
				>
					AGBs und Datenschutzrichtlinien
				</a>
			</Checkbox>
		</div>

		<Button type="submit" class="w-full mt-2">Stromvertrag abschließen</Button>
	</form>
</Modal>

<Modal title="Bankverbindung ändern" bind:open={editModal} outsideclose>
	<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
		Bitte füllen Sie das folgende Formular aus, um Ihre Bankverbindung zu ändern.
	</p>

	<form method="POST" action="?/update_contract" use:enhance>
		<input type="hidden" name="id" value={editContract.id} />
		<div class="grid gap-4 sm:grid-cols-2 sm:gap-6 mb-4">
			<Label class="space-y-2">
				<span>IBAN</span>
				<Input
					type="text"
					name="iban"
					placeholder="DE12378213781237"
					required
					value={editContract.iban}
				/>
			</Label>
			<Label class="space-y-2">
				<span>BIC</span>
				<Input type="text" name="blz" placeholder="COM81932XXX" required value={editContract.blz} />
			</Label>
		</div>
		<div class="flex items-start mb-2">
			<Checkbox>
				Ich stimme dem <a
					class="font-medium text-primary-600 hover:underline dark:text-primary-500 mx-1"
					href="/"
				>
					SEPA Lastschriftmandat
				</a>
				zu
			</Checkbox>
		</div>
		<hr class="my-4" />

		<div class="flex items-start mb-4">
			<Checkbox>
				Ich akzeptiere die <a
					class="font-medium text-primary-600 hover:underline dark:text-primary-500 ml-1"
					href="/"
				>
					AGBs und Datenschutzrichtlinien
				</a>
			</Checkbox>
		</div>

		<Button type="submit" class="w-full mt-2">Bankverbindung ändern</Button>
	</form>
</Modal>

<style>
</style>
