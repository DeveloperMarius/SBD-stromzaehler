<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Label, Input, Button, Card } from 'flowbite-svelte';
	import type { PageData } from './$types';
	import toast from 'svelte-french-toast';
	import { browser } from '$app/environment';

	export let data: PageData;
	let user = data.data.user;

	page.subscribe((pageData) => {
		if (browser && pageData.status != 200) {
			toast.error(pageData.form.error, {
				duration: 5000,
				position: 'top-right'
			});
		}

		user = pageData.data.data.user;
	});
</script>

<svelte:head>
	<title>Profildaten</title>
</svelte:head>

<div class="flex justify-between items-center w-full bg-white px-6 py-2 rounded-md mb-3 shadow-md">
	<h1 class="text-2xl">Ihre Daten</h1>
</div>

{#if user}
	{#key user}
		<Card padding="sm" class="max-w-full mb-4">
			<h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white mb-4">
				Profildaten aktualisieren
			</h5>
			<form
				class="flex flex-col space-y-6"
				method="POST"
				action="?/update_profile_data"
				use:enhance
			>
				<div class="grid gap-6 md:grid-cols-2">
					<Label class="space-y-2">
						<span>Vorname</span>
						<Input type="text" name="vorname" placeholder="Max" required value={user.vorname} />
					</Label>
					<Label class="space-y-2">
						<span>Nachname</span>
						<Input
							type="text"
							name="nachname"
							placeholder="Mustermensch"
							required
							value={user.nachname}
						/>
					</Label>
					<Label class="space-y-2">
						<span>Deine E-Mail</span>
						<Input
							type="email"
							name="_email"
							placeholder="name@company.com"
							disabled
							value={user.email}
						/>
					</Label>
					<Label class="space-y-2">
						<span>Deine Telefonnummer</span>
						<Input
							type="tel"
							name="telefon"
							placeholder="069 13232999"
							required
							value={user.telefon}
						/>
					</Label>
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
				<Button type="submit" class="w-full1">Daten aktualisieren</Button>
			</form>
		</Card>
		<Card padding="xl" class="max-w-full">
			<h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white mb-4">
				Passwort ändern
			</h5>

			<form class="flex flex-col space-y-6" method="POST" action="?/update_password" use:enhance>
				<div class="grid gap-6 md:grid-cols-2">
					<Label class="space-y-2">
						<span>Dein Passwort</span>
						<Input type="password" name="password" placeholder="•••••" required />
					</Label>
					<Label class="space-y-2">
						<span>Passwort bestätigen</span>
						<Input type="password" name="confirm-password" placeholder="•••••" required />
					</Label>
				</div>
				<Button type="submit" class="w-full1">Passwort ändern</Button>
			</form>
		</Card>
	{/key}
{:else}
	<p>Daten geladen ...</p>
{/if}

<style>
</style>
