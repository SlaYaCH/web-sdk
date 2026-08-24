<script lang="ts">
	import { Container, Rectangle, type SpineTrackProps } from 'pixi-svelte';

	import { SYMBOL_WIDTH, SYMBOL_HEIGHT } from '../game/constants';
	import { getSymbolInfo } from '../game/utils';
	import SymbolSpineMain from './SymbolSpineMain.svelte';

	type Props = {
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		x?: number;
		y?: number;
		listener: SpineTrackProps['listener'];
		showWinFrame: boolean;
		loop?: boolean;
	};

	const props: Props = $props();

	// ============================================================
	// LE CADRE DES SYMBOLES GAGNANTS
	//
	// Il venait de l'animation `payframe` du spine `anticipation`, le
	// dernier fichier du jeu d'exemple encore charge par Louvo. Il est
	// desormais dessine : deux rectangles, aucun fichier.
	//
	// Volontairement FIXE, sans pulsation. Jusqu'a 25 symboles peuvent
	// porter ce cadre en meme temps ; 25 animations recalculees a
	// chaque image coutent cher sur un telephone ancien, et ce sont
	// justement les appareils de votre liste de tests. Les lignes de
	// gain, elles, bougent deja.
	// ============================================================
	const COULEUR_CADRE = 0xff2d6a; // le rose de Louvo
	const COULEUR_LISERE = 0xffd166; // le dore du cadre de la grille
	const CADRE_LARGEUR = SYMBOL_WIDTH * 1.0;
	const CADRE_HAUTEUR = SYMBOL_HEIGHT * 1.0;
	const CADRE_EPAISSEUR = 3;
	const REMPLISSAGE = 0.12; // voile rose a l'interieur, 0 pour l'enlever
	const LISERE_LARGEUR = SYMBOL_WIDTH * 0.9;
	const LISERE_HAUTEUR = SYMBOL_HEIGHT * 0.88;
	const LISERE_EPAISSEUR = 2;
</script>

<!-- main -->
<SymbolSpineMain
	x={props.x}
	y={props.y}
	symbolInfo={props.symbolInfo}
	listener={props.listener}
	loop={props.loop}
/>

<!-- cadre du symbole gagnant -->
{#if props.showWinFrame}
	<Container x={props.x ?? 0} y={props.y ?? 0}>
		<Rectangle
			anchor={0.5}
			width={CADRE_LARGEUR}
			height={CADRE_HAUTEUR}
			backgroundColor={COULEUR_CADRE}
			backgroundAlpha={REMPLISSAGE}
			borderColor={COULEUR_CADRE}
			borderWidth={CADRE_EPAISSEUR}
		/>
		<Rectangle
			anchor={0.5}
			width={LISERE_LARGEUR}
			height={LISERE_HAUTEUR}
			backgroundColor={COULEUR_LISERE}
			backgroundAlpha={0}
			borderColor={COULEUR_LISERE}
			borderWidth={LISERE_EPAISSEUR}
		/>
	</Container>
{/if}
