<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { counterAnchor } from '../game/boardBox';
	import { anchorToPivot, BitmapText, Container, Rectangle, Sprite, type Sizes } from 'pixi-svelte';

	const context = getContext();

	const panelSizes = $derived({
		width: SYMBOL_SIZE * 1.53,
		height: SYMBOL_SIZE * 0.61,
	});
	// Miroir exact du compteur de free spins, a droite du centre de la grille.
	const ancre = $derived(counterAnchor(context.stateGame.tier));
	const position = $derived({
		// Miroir exact : meme ecartement que le compteur de
		// free spins, de l'autre cote du centre.
		x: ancre.centerX - panelSizes.width * 0.5 + SYMBOL_SIZE * 1.25,
		y: ancre.y,
	});

	const fontSize = SYMBOL_SIZE * 0.21;

	// --- VOTRE cadre a la place du caisson noir ---
	// total_win_frame.webp fait 1536x1024, soit un rapport de 1,5.
	// Le compteur, lui, fait 2,5 fois plus large que haut. On garde
	// donc la LARGEUR du compteur et on laisse la hauteur suivre le
	// rapport de l'image : le cadre grandit de part et d'autre,
	// centre, sans pousser la barre du bas. Rien n'est deforme.
	const CADRE = true; // <<< false pour revenir au caisson noir
	const CADRE_RATIO = 1536 / 1024; // proportions de l'image, a ne pas deformer
	// Le dessin n'occupe qu'environ la moitie de la hauteur du
	// sprite : a facteur 1, le cadre VISIBLE faisait 184 x 59,
	// soit moins haut que l'ancien caisson noir (184 x 73). D'ou
	// le texte a l'etroit. A 1.25 il fait 230 x 74.
	const CADRE_LARGEUR_FACTEUR = 1.25; // <<< elargir ou retrecir le cadre
	// Rattrapage vertical : recentre le DESSIN sur le texte,
	// et non le sprite. Mesure sur l'image elle-meme.
	const CADRE_DECALAGE_FRACTION = 0.0361; // <<< monter (negatif) ou descendre
	const CADRE_ETIRE = false; // <<< true = hauteur d'origine, image etiree
	const cadreLargeur = $derived(panelSizes.width * CADRE_LARGEUR_FACTEUR);
	const cadreHauteur = $derived(
		CADRE_ETIRE ? panelSizes.height : cadreLargeur / CADRE_RATIO,
	);
	// Visible UNIQUEMENT pendant les free spins (Speed Dating / After Dark) -
	// jamais en base game ni avec un simple mode active.
	const show = $derived(context.stateGame.gameType === 'freegame');

	let titleSizes: Sizes = $state({ width: 0, height: 0 });
	let amountSizes: Sizes = $state({ width: 0, height: 0 });
	const textContainerSizes = $derived({
		width: Math.max(titleSizes.width, amountSizes.width),
		height: titleSizes.height + amountSizes.height,
	});
</script>

<MainContainer>
	<FadeContainer {show} {...position} scale={1}>
		{#if CADRE}
			<Sprite
				anchor={0.5}
				x={panelSizes.width * 0.5}
				y={panelSizes.height * 0.5 + CADRE_DECALAGE_FRACTION * cadreHauteur}
				key="totalWinFrame"
				width={cadreLargeur}
				height={cadreHauteur}
			/>
		{:else}
			<Rectangle {...panelSizes} backgroundColor={0x000000} backgroundAlpha={0.78} />
		{/if}
		<Container
			x={panelSizes.width * 0.5}
			y={panelSizes.height * 0.48}
			pivot={anchorToPivot({
				sizes: textContainerSizes,
				anchor: { x: 0.5, y: 0.5 },
			})}
		>
			<BitmapText
				anchor={{ x: 0.5, y: 0 }}
				x={textContainerSizes.width * 0.5}
				text={'TOTAL WIN'}
				style={{
					fontFamily: 'gold', fill: 0xff2d6a,
					fontSize,
					wordWrap: false,
				}}
				onresize={(sizes) => (titleSizes = sizes)}
			/>
			<BitmapText
				anchor={{ x: 0.5, y: 0 }}
				x={textContainerSizes.width * 0.5}
				y={titleSizes.height}
				text={bookEventAmountToCurrencyString(stateBet.winBookEventAmount)}
				style={{
					fontFamily: 'gold', fill: 0xffffff,
					fontSize,
				}}
				onresize={(sizes) => (amountSizes = sizes)}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
