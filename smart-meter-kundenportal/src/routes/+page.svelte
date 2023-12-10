<script>
	import { Navbar, NavBrand, NavHamburger, NavUl, NavLi, Button } from 'flowbite-svelte';
	import { Section, HeroHeader } from 'flowbite-svelte-blocks';
	import { ArrowRightSolid } from 'flowbite-svelte-icons';
	import { Card } from 'flowbite-svelte';
	import {
		GlobeOutline,
		ComputerSpeakerSolid,
		FilePenOutline,
		MailBoxOutline,
		PhoneOutline
	} from 'flowbite-svelte-icons';
	import { Footer, FooterBrand, FooterLinkGroup, FooterLink } from 'flowbite-svelte';
	import { Heading, P } from 'flowbite-svelte';
	import {
		PricingBodyHead,
		PricingCard,
		PricingItemWrapper,
		PricingItem
	} from 'flowbite-svelte-blocks';
</script>

<svelte:head>
	<title>SmartStrom24 - Jetzt und nachhaltig</title>
</svelte:head>

<Navbar let:NavContainer color="none">
	<NavContainer class="border px-5 py-1 bg-white bg-opacity-50 backdrop-blur-md rounded-lg">
		<NavBrand href="/">
			<img
				class="self-center mr-3 h-6 sm:h-9 hover:scale-150 transition-all"
				src="/blitz.png"
				alt="blitz"
			/>
			<span class="self-center whitespace-nowrap text-xl font-semibold">SmartStrom24</span>
		</NavBrand>
		<div class="flex md:order-2">
			<a href="/auth/register">
				<Button size="sm">Registrieren</Button>
			</a>
			<NavHamburger />
		</div>
		<NavUl class="order-1 items-end">
			<NavLi href="/" active={true}>Home</NavLi>
			<NavLi href="#uberuns">Über uns</NavLi>
			<NavLi href="/docs/components/navbar">Preise</NavLi>
			<NavLi href="#angebote">Angebote</NavLi>
			<NavLi href="#kontakt">Kontakt</NavLi>
		</NavUl>
	</NavContainer>
</Navbar>
<div class="flex justify-center px-5 pt-2">
	<div class="py-20 max-w-screen-2xl grow bg-white bg-opacity-50 backdrop-blur-md rounded-lg">
		<Section name="heroVisual" class="border px-5 py-2 rounded-lg lg:grid lg:grid-cols-12">
			<div class="place-self-center lg:col-span-7">
				<HeroHeader
					h1Class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
					pClass="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400"
				>
					<svelte:fragment slot="h1">Willkommen bei SmartStrom24!</svelte:fragment>
					<svelte:fragment slot="paragraph">
						Unser Ziel ist es, die Energieerzeugung in Deutschland zu revolutionieren und
						nachhaltige Energie für alle zugänglich zu machen. Wir arbeiten mit den neuesten
						Technologien und erweitern kontinuierlich unser Portfolio an Projekten.
					</svelte:fragment>
					<a href="/auth/register">
						<Button size="xl" color="primary" class="inline-flex items-center justify-center mr-3">
							Jetzt loslegen <ArrowRightSolid size="md" class="ml-2 -mr-1" />
						</Button>
					</a>
				</HeroHeader>
			</div>
		</Section>
	</div>
</div>

<div class="px-5 py-10 flex justify-center" id="uberuns">
	<div class="py-10 bg-lighty-50 bg-opacity-70 backdrop-blur-md rounded-lg max-w-screen-2xl grow">
		<div class="px-5 pb-2 flex justify-center">
			<div class="justify-items-center text-center">
				<Heading tag="h1" class="mb-4">Warum wir?</Heading>
				<P class="text-center">Es gibt eine Menge an Vorteilen die Sie mit uns erleben werden</P>
			</div>
		</div>
		<div class="flex justify-center">
			<div class="features-grid gap-32 pt-2">
				<Card class="bg-opacity-0 backdrop-blur-md">
					<GlobeOutline class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
					<a href="/">
						<h5
							class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white text-center"
						>
							Erneuerbare Energiequellen
						</h5>
					</a>
					<p class="mb-3 font-normal text-gray-500 dark:text-gray-400 text-center">
						Wir schonen nachhaltige Methoden zur Energiegewinnung die Umwelt und tragen zur
						Reduzierung der Kohlenstoffemissionen bei
					</p>
				</Card>
				<Card class="bg-opacity-0 backdrop-blur-md">
					<ComputerSpeakerSolid class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
					<a href="/">
						<h5
							class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white text-center"
						>
							Smart Stromzähler
						</h5>
					</a>
					<p class="mb-3 font-normal text-gray-500 dark:text-gray-400 text-center">
						Wir verwenden neueste Technologie des Stromzählers und zeigen Ihre Stromdaten in der
						Echtzeit
					</p>
				</Card>
				<Card class="bg-opacity-0 backdrop-blur-md">
					<FilePenOutline class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
					<a href="/">
						<h5
							class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white text-center"
						>
							Schnell und einfach
						</h5>
					</a>
					<p class="mb-3 font-normal text-gray-500 dark:text-gray-400 text-center">
						Schließen Sie Ihren Vertrag mit uns reibungslos ab
					</p>
				</Card>
			</div>
		</div>
	</div>
</div>

<div class="px-5 pb-10 flex justify-center" id="angebote">
	<div class="py-10 bg-lighty-50 bg-opacity-70 backdrop-blur-md rounded-lg max-w-screen-2xl grow">
		<div class="px-5 pb-2 flex justify-center">
			<div class="justify-items-center text-center">
				<Heading tag="h1" class="mb-4">Unsere Angebote</Heading>
				<P class="text-center">Wählen Sie einen passenden Vertrag</P>
			</div>
		</div>

		<Section name="pricing">
			<div class="space-y-8 lg:grid lg:grid-cols-3 sm:gap-6 xl:gap-10 lg:space-y-0">
				<PricingCard class="bg-opacity-50 backdrop-blur-md">
					<PricingBodyHead>
						<svelte:fragment slot="h3">Standard</svelte:fragment>
						<svelte:fragment slot="paragraph">Standardvertrag mit fixer Laufzeit</svelte:fragment>
						<svelte:fragment slot="price">
							<span class="mr-2 text-5xl font-extrabold">55€</span>
							<span class="text-gray-500 dark:text-gray-400">/monat</span>
						</svelte:fragment>
					</PricingBodyHead>
					<PricingItemWrapper>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>Vertragslaufzeit: 24 Monate</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>Neukundenbonus: 24€</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>
								Arbeitspreis pro kWh: <span class="font-semibold">29,44 ct</span>
							</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>
								Grundpreis pro Monat: <span class="font-semibold">10,00 €</span>
							</span>
						</PricingItem>

						<svelte:fragment slot="btn">
							<Button color="primary" class="mt-4">Vertrag abschließen</Button>
						</svelte:fragment>
					</PricingItemWrapper>
				</PricingCard>

				<PricingCard class="bg-opacity-50 backdrop-blur-md">
					<PricingBodyHead>
						<svelte:fragment slot="h3">Flex-Tarif</svelte:fragment>
						<svelte:fragment slot="paragraph">Jederzeit kündbar</svelte:fragment>
						<svelte:fragment slot="price">
							<span class="mr-2 text-5xl font-extrabold">65€</span>
							<span class="text-gray-500 dark:text-gray-400">/monat</span>
						</svelte:fragment>
					</PricingBodyHead>
					<PricingItemWrapper>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>Vertragslaufzeit: 1 Monat</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>Flexibel</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>
								Arbeitspreis pro kWh: <span class="font-semibold">29,44 ct</span>
							</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>
								Grundpreis pro Monat: <span class="font-semibold">20,00 €</span>
							</span>
						</PricingItem>

						<svelte:fragment slot="btn">
							<Button color="primary" class="mt-4">Vertrag abschließen</Button>
						</svelte:fragment>
					</PricingItemWrapper>
				</PricingCard>

				<PricingCard class="bg-opacity-50 backdrop-blur-md">
					<PricingBodyHead>
						<svelte:fragment slot="h3">Preisgarantie</svelte:fragment>
						<svelte:fragment slot="paragraph">Langzeit-Festpreistarif</svelte:fragment>
						<svelte:fragment slot="price">
							<span class="mr-2 text-5xl font-extrabold">60€</span>
							<span class="text-gray-500 dark:text-gray-400">/monat</span>
						</svelte:fragment>
					</PricingBodyHead>
					<PricingItemWrapper>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>Vertragslaufzeit: 12 Monate</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>Preisgarantie: 12 Monate</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>
								Arbeitspreis pro kWh: <span class="font-semibold">28,51 ct</span>
							</span>
						</PricingItem>
						<PricingItem class="text-green-500 dark:text-green-400">
							<span>
								Grundpreis pro Monat: <span class="font-semibold">15,00 €</span>
							</span>
						</PricingItem>

						<svelte:fragment slot="btn">
							<Button color="primary" class="mt-4">Vertrag abschließen</Button>
						</svelte:fragment>
					</PricingItemWrapper>
				</PricingCard>
			</div>
		</Section>
	</div>
</div>

<div class="px-5 pb-10 flex justify-center" id="kontakt">
	<div class="py-10 bg-lighty-50 bg-opacity-70 backdrop-blur-md rounded-lg max-w-screen-2xl grow">
		<div class="px-5 pb-2 flex justify-center">
			<div class="justify-items-center text-center">
				<Heading tag="h1" class="mb-4">Kontaktiere uns</Heading>
				<P class="text-center">Wir sind für dich 24/7 erreichbar</P>
			</div>
		</div>
		<div class="flex justify-center">
			<div class="features-grid gap-32 pt-2">
				<Card class="bg-opacity-0 backdrop-blur-md w-72">
					<MailBoxOutline class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
					<a href="/">
						<h5
							class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white text-center"
						>
							Schreib uns
						</h5>
					</a>
					<p class="mb-3 font-normal text-gray-500 dark:text-gray-400 text-center">
						info@smartstrom24.top
					</p>
				</Card>
				<Card class="bg-opacity-0 backdrop-blur-md w-72">
					<PhoneOutline class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
					<a href="/">
						<h5
							class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white text-center"
						>
							Ruf uns an
						</h5>
					</a>
					<p class="mb-3 font-normal text-gray-500 dark:text-gray-400 text-center">0800 666 6969</p>
				</Card>
			</div>
		</div>
	</div>
</div>

<div class="pt-5">
	<Footer footerType="socialmedia" class="bg-primary-600 bg-opacity-50 backdrop-blur-md">
		<div class="mx-auto max-w-screen-xl text-center">
			<FooterBrand
				href="smartstrom24.top"
				src="/blitz.png"
				alt="Unser Logo"
				name="SmartStrom24"
				aClass="flex justify-center items-center text-2xl font-semibold text-gray-900 dark:text-white"
			/>
			<p class="my-6 text-primary-900 dark:text-gray-400">
				Ihr Anbieter für den nachhaltigen Strom
			</p>
			<FooterLinkGroup
				ulClass="flex flex-wrap justify-center items-center mb-6 text-gray-900 dark:text-white"
			>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">About</FooterLink>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Premium</FooterLink>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Campaigns</FooterLink>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Blog</FooterLink>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">
					Affiliate Program
				</FooterLink>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">FAQs</FooterLink>
				<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Contact</FooterLink>
			</FooterLinkGroup>
			<span class="text-sm text-primary-900 sm:text-center dark:text-gray-400">
				© 2023 <a href="https://flowbite.com/" class="hover:underline">SmartStrom24™</a>
				. All Rights Reserved.
			</span>
		</div>
	</Footer>
</div>

<style lang="scss">
	:global(body) {
		background: url('/background.png') no-repeat center center fixed;
		background-size: cover;
	}

	:global(.feature-item) {
		background: rgba(255, 255, 255, 0.3); /* weißer Hintergrund mit Transparenz */
		backdrop-filter: blur(10px); /* unscharfer Hintergrund-Effekt */
		border-radius: 1rem; /* runde Ecken */
		margin: 1rem; /* Abstand zwischen den Elementen */
		padding: 1rem; /* Innenabstand */
		width: calc(33.333% - 2rem); /* Berechnung der Breite jedes Elements, minus Margin */
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* leichter Schatten für Tiefe */
	}

	.features-grid {
		display: flex;
		justify-content: space-around; /* sorgt für gleichmäßigen Abstand */
		flex-wrap: wrap; /* sorgt dafür, dass Elemente in eine neue Zeile umbrechen, wenn der Bildschirm zu klein wird */
	}

	@media screen and (max-width: 768px) {
		.feature-item {
			width: calc(50% - 2rem); /* Anpassung für kleinere Bildschirme */
		}
	}

	@media screen and (max-width: 480px) {
		.feature-item {
			width: 100%; /* Anpassung für Mobilgeräte */
		}
	}
</style>
