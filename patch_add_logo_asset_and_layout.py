results = []

# --- 1) Enregistrer le logo comme asset Pixi ---
path1 = "apps/louvo/src/game/assets.ts"
with open(path1, "r") as f:
    c1 = f.read()

old1 = "} as const;"
new1 = """	louvoLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_logo.png', import.meta.url).href,
	},
} as const;"""

count1 = c1.count(old1)
if count1 != 1:
    results.append(f"ERREUR (assets.ts) : trouve {count1} fois (attendu 1).")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK (assets.ts) : logo enregistre comme asset 'louvoLogo'.")

# --- 2) Brancher le nouvel ecran de chargement Louvo dans +layout.svelte ---
path2 = "apps/louvo/src/routes/+layout.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoaderStakeEngine, LoaderExample, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import messagesMap from '../i18n/messagesMap';
	type Props = { children: Snippet };
	const props: Props = $props();
	let showYourLoader = $state(false);
	const loaderUrlStakeEngine = new URL('../../stake-engine-loader.gif', import.meta.url).href;
	const loaderUrl = new URL('../../loader.gif', import.meta.url).href;
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
	<LoaderExample src={loaderUrl} />
	<!-- '/loader.gif' is served from static folder of sveltekit -->
	<!-- File location: apps/scatter/static/loader.gif -->
{/if}
{@render props.children()}"""

new2 = """<script lang="ts">
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
{@render props.children()}"""

count2 = c2.count(old2)
if count2 != 1:
    results.append(f"ERREUR (+layout.svelte) : trouve {count2} fois (attendu 1) - le fichier a peut-etre change, verification manuelle necessaire.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK (+layout.svelte) : ecran de chargement Louvo branche, logo au lieu de loader.gif generique.")

for r in results:
    print(r)
