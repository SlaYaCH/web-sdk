<script lang="ts">
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';
	import { getContext } from '../game/context';
	import Ambience from './Ambience.svelte';

	const context = getContext();

	const showBaseBackground = $derived(
		context.stateGame.gameType === 'basegame' || context.stateGame.tier === 'speed_dating',
	);
	const showFeatureBackground = $derived(context.stateGame.tier === 'after_dark');

	// ------------------------------------------------------------------
	// Le fond ne contient plus la grille ni l'enseigne : il n'y a donc plus
	// rien a aligner avec le cadre. Il s'etire simplement sur tout le canvas,
	// quelle que soit la forme de l'ecran. Plus de bande vide a combler,
	// plus de jointure a maquiller.
	// ------------------------------------------------------------------
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const etire = $derived({
		x: canvas.width * 0.5,
		y: canvas.height * 0.5,
		width: canvas.width,
		height: canvas.height,
	});
</script>

<Rectangle {...canvas} backgroundColor={0x000000} zIndex={-4} />

<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-3}>
	<Ambience mode="base" cle="boardBackground" actif={showBaseBackground} />
</FadeContainer>

<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-2}>
	<Ambience mode="afterDark" cle="boardBackgroundAfterDark" actif={showFeatureBackground} />
</FadeContainer>
