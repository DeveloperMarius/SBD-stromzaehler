<script>
	import { Navbar, NavBrand, NavHamburger, NavUl, NavLi, Button } from 'flowbite-svelte';
	import { Section, HeroHeader } from 'flowbite-svelte-blocks';
	import { ArrowRightSolid } from 'flowbite-svelte-icons';
	import { Card } from 'flowbite-svelte';
	import { FeatureDefault, FeatureItem } from 'flowbite-svelte-blocks';
	import { ChartSolid, LandmarkSolid, BriefcaseSolid, DollarSolid, RocketSolid, CogOutline } from 'flowbite-svelte-icons';
	import { Footer, FooterBrand, FooterLinkGroup, FooterLink, FooterCopyright, FooterIcon } from 'flowbite-svelte';
	import { Portfolio, PortfolioItem } from 'flowbite-svelte-blocks';
	import { GiftBoxSolid, ArrowUpRightFromSquareOutline } from 'flowbite-svelte-icons';
	import { Heading, P } from 'flowbite-svelte';
	import { PricingBodyHead, PricingCard, PricingItemWrapper, PricingHead, PricingItem } from 'flowbite-svelte-blocks';
</script>

<svelte:head>
	<title>SmartStrom24 - Jetzt und nachhaltig</title>
</svelte:head>


<Navbar let:NavContainer color="none">
	<NavContainer class="border px-5 py-1 bg-white bg-opacity-50 backdrop-blur-md rounded-lg">
		<NavBrand href="/">
			<img class="self-center mr-3 h-6 sm:h-9 hover:scale-150 transition-all" src="/blitz.png" alt ="blitz" >
			<span class="self-center whitespace-nowrap text-xl font-semibold">SmartStrom24</span>
		</NavBrand>
		<div class="flex md:order-2">
			<a href="/auth/register">
				<Button size="sm">Anmelden</Button>
			</a>
			<NavHamburger />
		</div>
		<NavUl class="order-1 items-end">
			<NavLi href="/" active={true}>Home</NavLi>
			<NavLi href="/about">Über uns</NavLi>
			<NavLi href="/docs/components/navbar">Preise</NavLi>
			<NavLi href="/pricing">Angebote</NavLi>
			<NavLi href="/contact">Kontakt</NavLi>
		  </NavUl>
	</NavContainer>
</Navbar>
<div class = "px-5 pt-2">
<div class = "pb-5 py-3 bg-white bg-opacity-50 backdrop-blur-md rounded-lg">
<Section name="heroVisual" class="border px-5 py-2 rounded-lg lg:grid lg:grid-cols-12">
<div class="place-self-center lg:col-span-7 ">
	<HeroHeader h1Class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white" pClass="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">
		<svelte:fragment slot="h1">Willkommen bei SmartStrom24!</svelte:fragment>
		<svelte:fragment slot="paragraph">Unser Ziel ist es, die Energieerzeugung in Deutschland zu revolutionieren und nachhaltige
			Energie für alle zugänglich zu machen. Wir arbeiten mit den neuesten Technologien und
			erweitern kontinuierlich unser Portfolio an Projekten.</svelte:fragment>
		<a href="/"><Button size="xl" color="red" class="inline-flex items-center justify-center mr-3">Get started<ArrowRightSolid size="md" class="ml-2 -mr-1" /></Button> </a>
		<a href="/"><Button color="light" size="xl" class="inline-flex items-center justify-center">Speak to Sales</Button> </a>
		</HeroHeader>
</div>
</Section>
</div>
</div>

<div class="px-5 py-5">
<div class="px-5 pb-2 bg-white bg-opacity-50 backdrop-blur-md justify-items-center text-center rounded-lg">
	<Heading tag="h1" class="mb-4">Warum wir?</Heading>
	<P class="text-center">Es gibt eine Menge an Vorteilen die Sie mit uns erleben werden</P>
</div>
<div class="features-grid pt-2">
	<Card class="bg-opacity-50 backdrop-blur-md">
		<GiftBoxSolid class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
		<a href="/">
		  <h5 class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Erneuerbare Energiequellen</h5>
		</a>
		<p class="mb-3 font-normal text-gray-500 dark:text-gray-400">Wir schonen nachhaltige Methoden zur Energiegewinnung die Umwelt und tragen zur Reduzierung der Kohlenstoffemissionen bei</p>

	  </Card>
	  <Card class="bg-opacity-50 backdrop-blur-md">
		<GiftBoxSolid class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
		<a href="/">
		  <h5 class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Smart Stromzähler</h5>
		</a>
		<p class="mb-3 font-normal text-gray-500 dark:text-gray-400">Wir verwenden neueste Technologie des Stromzählers und zeigen Ihre Stromdaten in der Echtzeit</p>

	  </Card>
	  <Card class="bg-opacity-50 backdrop-blur-md">
		<GiftBoxSolid class="w-7 h-7 mb-3 text-gray-500 dark:text-gray-400 self-center" />
		<a href="/">
		  <h5 class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Schnell und einfach</h5>
		</a>
		<p class="mb-3 font-normal text-gray-500 dark:text-gray-400">Schließen Sie Ihren Vertrag mit uns reibungslos ab</p>

	  </Card>

</div>
</div>

<div class="px-5 py-5">
<div class="px-5 pb-2 bg-white bg-opacity-50 backdrop-blur-md justify-items-center text-center rounded-lg">
	<Heading tag="h1" class="mb-4">Unsere Angebote</Heading>
	<P class="text-center">Wählen Sie einen passenden Vertrag</P>
</div>
</div>

<Section name="pricing">
<div class="space-y-8 lg:grid lg:grid-cols-3 sm:gap-6 xl:gap-10 lg:space-y-0">
	<PricingCard class= "bg-opacity-50 backdrop-blur-md">
	<PricingBodyHead>
		<svelte:fragment slot="h3">Eco</svelte:fragment>
		<svelte:fragment slot="paragraph">einfach</svelte:fragment>
		<svelte:fragment slot="price">
		<span class="mr-2 text-5xl font-extrabold">29€</span>
		<span class="text-gray-500 dark:text-gray-400">/monat</span>
		</svelte:fragment>
	</PricingBodyHead>
	<PricingItemWrapper>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Individual configuration</span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>No setup, or hidden fees</span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Team size: <span class="font-semibold">1 developer</span></span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Premium support: <span class="font-semibold">6 months</span></span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Free updates: <span class="font-semibold">6 months</span></span>
		</PricingItem>

		<svelte:fragment slot="btn">
		<Button color="red">Vertrag abschließen</Button>
		</svelte:fragment>
	</PricingItemWrapper>
	</PricingCard>

	<PricingCard class= "bg-opacity-50 backdrop-blur-md">
	<PricingBodyHead>
		<svelte:fragment slot="h3">Standart</svelte:fragment>
		<svelte:fragment slot="paragraph">bessere support.</svelte:fragment>
		<svelte:fragment slot="price">
		<span class="mr-2 text-5xl font-extrabold">99€</span>
		<span class="text-gray-500 dark:text-gray-400">/monat</span>
		</svelte:fragment>
	</PricingBodyHead>
	<PricingItemWrapper>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Individual configuration</span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>No setup, or hidden fees</span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Team size: <span class="font-semibold">10 developer</span></span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Premium support: <span class="font-semibold">24 months</span></span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Free updates: <span class="font-semibold">24 months</span></span>
		</PricingItem>

		<svelte:fragment slot="btn">
		<Button color="red">Vertrag abschließen</Button>
		</svelte:fragment>
	</PricingItemWrapper>
	</PricingCard>

	<PricingCard class= "bg-opacity-50 backdrop-blur-md">
	<PricingBodyHead>
		<svelte:fragment slot="h3">Premium</svelte:fragment>
		<svelte:fragment slot="paragraph">Best support</svelte:fragment>
		<svelte:fragment slot="price">
		<span class="mr-2 text-5xl font-extrabold">$120€</span>
		<span class="text-gray-500 dark:text-gray-400">/monat</span>
		</svelte:fragment>
	</PricingBodyHead>
	<PricingItemWrapper>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Individual configuration</span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>No setup, or hidden fees</span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Team size: <span class="font-semibold">100+ developer</span></span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Premium support: <span class="font-semibold">36 months</span></span>
		</PricingItem>
		<PricingItem class="text-green-500 dark:text-green-400">
		<span>Free updates: <span class="font-semibold">36 months</span></span>
		</PricingItem>

		<svelte:fragment slot="btn">
		<Button color="red">Vertrag abschließen</Button>
		</svelte:fragment>
	</PricingItemWrapper>
	</PricingCard>
</div>
</Section>

<div class="pt-5">
<Footer footerType="socialmedia" class="bg-primary-600 bg-opacity-50 backdrop-blur-md">
	<div class="mx-auto max-w-screen-xl text-center">
	  <FooterBrand href="smartstrom24.de" src="/blitz.png" alt="Unser Logo" name="SmartStrom24" aClass="flex justify-center items-center text-2xl font-semibold text-gray-900 dark:text-white" />
	  <p class="my-6 text-primary-900 dark:text-gray-400">Ihr Anbieter für den nachhaltigen Strom</p>
	  <FooterLinkGroup ulClass="flex flex-wrap justify-center items-center mb-6 text-gray-900 dark:text-white">
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">About</FooterLink>
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Premium</FooterLink>
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Campaigns</FooterLink>
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Blog</FooterLink>
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Affiliate Program</FooterLink>
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">FAQs</FooterLink>
		<FooterLink liClass="" aClass="mr-4 hover:underline md:mr-6" href="/">Contact</FooterLink>
	  </FooterLinkGroup>
	  <span class="text-sm text-primary-900 sm:text-center dark:text-gray-400">© 2023 <a href="https://flowbite.com/" class="hover:underline">SmartStrom24™</a>. All Rights Reserved.</span>
	</div>
  </Footer>
</div>

<style lang="scss">
	
:global( .feature-item) {
	background: rgba(255, 255, 255, 0.3); /* weißer Hintergrund mit Transparenz */
	backdrop-filter: blur(10px); /* unscharfer Hintergrund-Effekt */
	border-radius: 1rem; /* runde Ecken */
	margin: 1rem; /* Abstand zwischen den Elementen */
	padding: 1rem; /* Innenabstand */
	width: calc(33.333% - 2rem); /* Berechnung der Breite jedes Elements, minus Margin */
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* leichter Schatten für Tiefe */
}
.features-container {
    /* Container-Styling */
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