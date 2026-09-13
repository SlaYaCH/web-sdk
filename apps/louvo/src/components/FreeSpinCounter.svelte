<script lang="ts" module>
	export type EmitterEventFreeSpinCounter =
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { counterAnchor } from '../game/boardBox';
	import { anchorToPivot, BitmapText, Container, Rectangle, Sprite, type Sizes } from 'pixi-svelte';

	const context = getContext();
	const PANEL_KEY_DESKTOP = 'Frame_FSCounter.png';
	const PANEL_RATIO_DESKTOP = 824 / 622;
	const panelKey = PANEL_KEY_DESKTOP;
	const panelWidth = $derived(SYMBOL_SIZE * 1.53);
	const panelSizes = $derived({
		width: panelWidth,
		height: SYMBOL_SIZE * 0.61,
	});
	const scale = 1;
	// Ancre commune aux deux compteurs : le bas REEL de la grille, lu dans
	// la boite de cadre. Voir counterAnchor dans boardBox.ts.
	const ancre = $derived(counterAnchor(context.stateGame.tier));
	const position = $derived({
		// Ecartement des deux compteurs. Il suit la largeur du
		// cadre : plus large, il faut les eloigner pour qu'ils
		// ne se touchent pas au centre.
		x: ancre.centerX - panelSizes.width * 0.5 - SYMBOL_SIZE * 1.25,
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

	let show = $state(false);
	let current = $state(0);
	let total = $state(0);
	let titleSizes: Sizes = $state({ width: 0, height: 0 });
	let counterSizes: Sizes = $state({ width: 0, height: 0 });

	const textContainerSizes = $derived({
		width: titleSizes.width,
		height: titleSizes.height + counterSizes.height,
	});
	const counterPosition = $derived({ x: titleSizes.width / 2, y: titleSizes.height });

	context.eventEmitter.subscribeOnMount({
		freeSpinCounterShow: () => (show = true),
		freeSpinCounterHide: () => (show = false),
		freeSpinCounterUpdate: (emitterEvent) => {
			if (emitterEvent.current !== undefined) current = emitterEvent.current;
			if (emitterEvent.total !== undefined) total = emitterEvent.total;
		},
	});
</script>

<MainContainer>
	<FadeContainer {show} {...position} {scale}>
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
				text={'FREE SPIN'}
				style={{
					fontFamily: 'gold', fill: 0xff2d6a,
					fontSize,
					wordWrap: false,
				}}
				onresize={(sizes) => (titleSizes = sizes)}
			/>
			<BitmapText
				text={`${current} OF ${total}`}
				{...counterPosition}
				anchor={{ x: 0.5, y: 0 }}
				style={{
					fontFamily: 'gold', fill: 0xffffff,
					fontSize,
				}}
				onresize={(sizes) => (counterSizes = sizes)}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
