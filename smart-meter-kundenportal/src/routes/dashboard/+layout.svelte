<script lang="ts">
	import { page } from '$app/stores';
	import { SidebarBottomNav, SidebarBottomNavItem } from 'flowbite-svelte-blocks';
	import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper } from 'flowbite-svelte';
	$: activeUrl = $page.url.pathname;

	import {
		HomeOutline,
		ArrowLeftToBracketOutline,
		FileLinesOutline,
		LightbulbOutline,
		WalletOutline,
		UserSettingsOutline
	} from 'flowbite-svelte-icons';
</script>

<svelte:head>
	<title>Dashboard</title>
</svelte:head>

<div class="flex min-h-screen">
	<Sidebar class="h-screen shadow-md" bind:activeUrl>
		<SidebarWrapper class="min-h-screen relative">
			<SidebarGroup class="mb-4">
				<div class="flex items-center">
					<img class="w-12" src="/logo_house.png" alt="Logo" />
					<h3 class="font-serif font-bold ml-2">SmartStrom24.jetzt</h3>
				</div>
			</SidebarGroup>

			<SidebarGroup border>
				<SidebarItem label="Übersicht" href="/dashboard">
					<svelte:fragment slot="icon">
						<HomeOutline size="sm" />
					</svelte:fragment>
				</SidebarItem>
			</SidebarGroup>
			<SidebarGroup>
				<SidebarItem label="Ihre Verträge" href="/dashboard/contracts">
					<svelte:fragment slot="icon">
						<FileLinesOutline size="sm" />
					</svelte:fragment>
				</SidebarItem>
			</SidebarGroup>
			<SidebarGroup>
				<SidebarItem label="Ihre Kosten" href="/dashboard/cost-analysis">
					<svelte:fragment slot="icon">
						<WalletOutline size="sm" />
					</svelte:fragment>
				</SidebarItem>
			</SidebarGroup>
			<SidebarGroup>
				<SidebarItem label="Ihre Stromzähler" href="/dashboard/smart-meter">
					<svelte:fragment slot="icon">
						<LightbulbOutline size="sm" />
					</svelte:fragment>
				</SidebarItem>
			</SidebarGroup>
			<SidebarGroup>
				<SidebarItem label="Ihre Daten" href="/dashboard/profile">
					<svelte:fragment slot="icon">
						<UserSettingsOutline size="sm" />
					</svelte:fragment>
				</SidebarItem>
			</SidebarGroup>
			<SidebarBottomNav
				divClass="absolute bottom-0 left-0 justify-center p-4 space-x-4 w-full lg:flex bg-white dark:bg-gray-800 z-20"
			>
				<SidebarBottomNavItem href="/auth/logout" tooltip="Logout">
					<ArrowLeftToBracketOutline />
				</SidebarBottomNavItem>
			</SidebarBottomNav>
		</SidebarWrapper>
	</Sidebar>
	<main>
		<slot>Hier steht HTML von die Dashboard ding</slot>
	</main>
</div>

<style lang="scss">
	:global(body) {
		@apply bg-slate-50 overflow-hidden;
	}

	main {
		@apply max-h-screen overflow-y-auto flex-grow px-5 py-3;
	}
</style>
