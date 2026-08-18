<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoaderStakeEngine, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import LouvoLoaderLogo from '../components/LouvoLoaderLogo.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();

	let showYourLoader = $state(false);

	const loaderUrlStakeEngine = new URL('../../stake-engine-loader.gif', import.meta.url).href;
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

<LoaderStakeEngine src={loaderUrlStakeEngine} oncomplete={() => (showYourLoader = true)} />

{#if showYourLoader}
	<LouvoLoaderLogo src={loaderUrl} />
{/if}

{@render props.children()}