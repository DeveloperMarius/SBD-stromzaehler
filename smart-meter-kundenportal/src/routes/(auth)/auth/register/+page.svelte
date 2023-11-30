<script lang="ts">
	import { Section, Register } from 'flowbite-svelte-blocks';
	import { Button, Checkbox, Label, Input } from 'flowbite-svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>Registrieren</title>
	<meta name="description" content="Registrieren" />
	<meta name="robots" content="noindex" />
</svelte:head>

<div class="flex justify-center items-center h-screen">
	<Section name="register" sectionClass="relative md:w-1/2 sm:3/4 w-11/12">
		<Register href="/">
			<div class="p-6 space-y-4 md:space-y-6 sm:p-8 w-">
				<form class="flex flex-col space-y-6" method="POST" action="?/register" use:enhance>
					<h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Registrieren</h3>
					{#if $page.status != 200}<p class="text-red-700">{$page.form.error}</p>{/if}
					<div class="grid gap-6 mb-6 md:grid-cols-2">
						<Label class="space-y-2">
							<span>Vorname</span>
							<Input type="text" name="vorname" placeholder="Max" required />
						</Label>
						<Label class="space-y-2">
							<span>Nachname</span>
							<Input type="text" name="nachname" placeholder="Mustermensch" required />
						</Label>
					</div>
					<Label class="space-y-2">
						<span>Deine E-Mail</span>
						<Input type="email" name="email" placeholder="name@company.com" required />
					</Label>
					<Label class="space-y-2">
						<span>Deine Telefonnummer</span>
						<Input type="tel" name="telefon" placeholder="069 13232999" required />
					</Label>
					<Label class="space-y-2">
						<span>Dein Passwort</span>
						<Input type="password" name="password" placeholder="•••••" required />
					</Label>
					<Label class="space-y-2">
						<span>Passwort bestätigen</span>
						<Input type="password" name="confirm-password" placeholder="•••••" required />
					</Label>
					<div class="grid gap-6 mb-6 md:grid-cols-2">
						<Label class="space-y-2">
							<span>Straße</span>
							<Input type="text" name="strasse" placeholder="Schlossallee" required />
						</Label>
						<Label class="space-y-2">
							<span>Hausnummer</span>
							<Input type="text" name="hausnr" placeholder="400" required />
						</Label>
						<Label class="space-y-2">
							<span>Ort</span>
							<Input type="text" name="ort" placeholder="Musterstadt" required />
						</Label>
						<Label class="space-y-2">
							<span>Postleitzahl</span>
							<Input type="text" name="plz" placeholder="12345" required />
						</Label>
					</div>
					<div class="flex items-start">
						<Checkbox
							>Ich akzeptiere die <a
								class="font-medium text-primary-600 hover:underline dark:text-primary-500 ml-1"
								href="/"
							>
								AGBs und Datenschutzrichtlinien</a
							></Checkbox
						>
					</div>
					<Button type="submit" class="w-full1">Account erstellen</Button>
					<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
						Du hast bereits einen Account? <a
							href="/auth/login"
							class="font-medium text-primary-600 hover:underline dark:text-primary-500"
							>Hier anmelden</a
						>
					</div>
				</form>
			</div>
		</Register>
	</Section>
</div>
