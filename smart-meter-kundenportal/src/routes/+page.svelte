<script>
	import { Navbar, NavBrand, NavHamburger, NavLi, Button } from 'flowbite-svelte';
	import { Section, HeroHeader } from 'flowbite-svelte-blocks';
	import { ArrowRightSolid } from 'flowbite-svelte-icons';
</script>

<Navbar let:NavContainer color="none">
	<NavContainer class="border px-5 py-2 rounded-lg bg-white">
		<NavBrand href="/">
			<img class="self-center mr-3 h-6 sm:h-9 hover:scale-125 transition-all" src="/blitz.png" alt ="blitz" >
			<span class="self-center whitespace-nowrap text-xl font-semibold">SmartStrom24</span>
		</NavBrand>
		<NavHamburger />
		<div class="flex md:order-2">
			<a href="/auth/register">
				<Button size="sm">Jetzt loslegen!</Button>
			</a>
			<NavHamburger />
		</div>
	</NavContainer>
</Navbar>

<Section name="heroVisual">
	<div class="mr-auto place-self-center lg:col-span-7 my-36">
		<HeroHeader
			h1Class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
			pClass="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400"
		>
			<svelte:fragment slot="h1">Willkommen bei SmartStrom24</svelte:fragment>
			<svelte:fragment slot="paragraph">
				Unser Ziel ist es, die Energieerzeugung in Deutschland zu revolutionieren und nachhaltige
				Energie für alle zugänglich zu machen. Wir arbeiten mit den neuesten Technologien und
				erweitern kontinuierlich unser Portfolio an Projekten.
			</svelte:fragment>
			<a href="/"
				><Button size="xl" color="red" class="inline-flex items-center justify-center mr-3"
					>Get started<ArrowRightSolid size="md" class="ml-2 -mr-1" /></Button
				>
			</a>
			<a href="/"
				><Button color="light" size="xl" class="inline-flex items-center justify-center"
					>Speak to Sales</Button
				>
			</a>
		</HeroHeader>
	</div>
</Section>
