<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import LouvoLoaderLogo from '../components/LouvoLoaderLogo.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();

	// Le loader Stake Engine a ete retire : la checklist d'approbation
	// l'interdit ("Game should not contain the Stake Engine Loader").
	// C'est lui qui basculait cette valeur a true une fois termine ;
	// sans lui, l'ecran de chargement Louvo prend la main des le depart.
	let showYourLoader = $state(true);

	const loaderUrl = new URL('../../louvo_logo.png', import.meta.url).href;

	setContext();
</script>

<GlobalStyle>
	<Authenticate>
		<LoadI18n {messagesMap}>
			<Game />
		</LoadI18n>
	</Authenticate>
</GlobalStyle>

{#if showYourLoader}
	<LouvoLoaderLogo src={loaderUrl} />
{/if}

{@render props.children()}