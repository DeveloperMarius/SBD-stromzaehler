<script lang="ts">
	import { Section, Register } from 'flowbite-svelte-blocks';
	import { Button, Checkbox, Label, Input } from 'flowbite-svelte';
</script>

<div class="flex justify-center items-center h-screen">
	<Section name="register" sectionClass="relative md:w-1/2 sm:3/4 w-11/12">
		<Register href="/">
			<div class="p-6 space-y-4 md:space-y-6 sm:p-8 w-">
				<form class="flex flex-col space-y-6" action="/">
					<h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Account erstellen</h3>
					<Label class="space-y-2">
						<span>Deine E-Mail</span>
						<Input type="email" name="email" placeholder="name@company.com" required />
					</Label>
					<Label class="space-y-2">
						<span>Dein Passwort</span>
						<Input type="password" name="password" placeholder="•••••" required />
					</Label>
					<Label class="space-y-2">
						<span>Passwort bestätigen</span>
						<Input type="password" name="confirm-password" placeholder="•••••" required />
					</Label>
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
