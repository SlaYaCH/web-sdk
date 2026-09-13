<script lang="ts" module>
	export type EmitterEventFreeSpinIntro =
		| { type: 'freeSpinIntroShow'; tier?: string }
		| { type: 'freeSpinIntroHide' }
		| { type: 'freeSpinIntroUpdate'; totalFreeSpins: number };
</script>

<script lang="ts">
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { stateUrlDerived } from 'state-shared';
	import { FadeContainer } from 'components-pixi';
	import { waitForResolve } from 'utils-shared/wait';
	import { BitmapText, Container, Rectangle, SpineProvider, SpineSlot, SpineTrack, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import PressToContinue from './PressToContinue.svelte';
	import FreeSpinAnimation from './FreeSpinAnimation.svelte';

	type AnimationName = 'intro' | 'idle';

	const context = getContext();

	let show = $state(false);
	let animationName = $state<AnimationName>('intro');
	let freeSpinsFromEvent = $state(0);
	// Image d'annonce : le tier arrive AVEC l'evenement d'ouverture - ne pas
	// lire stateGame.tier, pose 450 ms plus tard exprès (changement de decor
	// cache sous l'annonce), ce qui faisait flasher l'image Speed Dating.
	let announceTier = $state('speed_dating');
	let oncomplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		freeSpinIntroShow: (emitterEvent) => {
			announceTier = emitterEvent.tier ?? 'speed_dating';
			show = true;
		},
		freeSpinIntroHide: () => (show = false),
		freeSpinIntroUpdate: async (emitterEvent) => {
			// if (emitterEvent.extraSpins) {
			// 	context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fs_respins' });
			// }
			// freeSpinsFromEvent = emitterEvent.extraSpins ?? emitterEvent.totalFreeSpins;
			freeSpinsFromEvent = emitterEvent.totalFreeSpins;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});

	// --- VOTRE cadre derriere l'annonce, au lieu du fond noir ---
	// Meme element pour Speed Dating et pour After Dark : une
	// seule modification couvre les deux ecrans.
	const CADRE_INTRO = true; // <<< false pour revenir au fond noir
	const CADRE_INTRO_LARGEUR = context.stateLayoutDerived.mainLayout().width * 0.24; // reprise du rectangle noir
	const CADRE_INTRO_RATIO = 1536 / 1024;
	// Recentre l'INTERIEUR du cadre sur le texte, pas la toile.
	const CADRE_INTRO_DECALAGE = 0.0361; // <<< monter (negatif) ou descendre
	const cadreIntroHauteur = CADRE_INTRO_LARGEUR / CADRE_INTRO_RATIO;
	// Taille du texte de l'annonce. Etait a 0.055 : il debordait du
	// panneau et mordait sur les ornements.
	const TEXTE_TAILLE = context.stateLayoutDerived.mainLayout().height * 0.050; // <<< LA taille du texte
	// Hauteur du bloc d'annonce sur l'ecran. Il etait a 0.88, ce qui
	// convenait au rectangle noir (0,085 de haut). Votre cadre garde
	// ses proportions 3:2 : a la meme largeur il fait ~0,285 de la
	// hauteur de l'ecran, soit TROIS FOIS PLUS. A 0.88 son bas
	// sortirait de l'ecran et il recouvrirait TAP TO CONTINUE.
	const ANNONCE_Y = 0.79; // <<< remonter (plus petit) ou descendre
	// Descend TAP TO CONTINUE, sur CET ecran seulement.
	const TAP_DECALAGE = 25; // <<< en pixels, vers le bas
</script>

<FadeContainer {show}>
	<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />
	<MainContainer>
		<Sprite
			anchor={0.5}
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.5}
			width={context.stateLayoutDerived.mainLayout().width}
			height={context.stateLayoutDerived.mainLayout().height}
			key={announceTier === 'after_dark' ? 'afterDarkAnnounce' : 'speedDatingAnnounce'}
		/>
	</MainContainer>


	<MainContainer>
		<Container
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * ANNONCE_Y}
		>
			{#if CADRE_INTRO}
				<!-- Ancre au CENTRE, donc x et y sont le centre du cadre :
					zero, comme le texte juste en dessous. Le rectangle noir de
					repli, lui, n'a pas d'ancre - ses coordonnees partent du
					coin haut-gauche et restent donc negatives. Les deux
					branches ne suivent pas la meme regle, exprès. -->
				<Sprite
					anchor={0.5}
					x={0}
					y={CADRE_INTRO_DECALAGE * cadreIntroHauteur}
					key="totalWinFrame"
					width={CADRE_INTRO_LARGEUR}
					height={cadreIntroHauteur}
				/>
			{:else}
				<Rectangle
					x={-context.stateLayoutDerived.mainLayout().width * 0.12}
					y={-context.stateLayoutDerived.mainLayout().height * 0.0425}
					width={context.stateLayoutDerived.mainLayout().width * 0.24}
					height={context.stateLayoutDerived.mainLayout().height * 0.085}
					backgroundColor={0x000000}
					backgroundAlpha={0.78}
				/>
			{/if}
			<BitmapText
				anchor={{ x: 0.5, y: 0.5 }}
				text={`${freeSpinsFromEvent} FREE SPINS`}
				style={{
					fontFamily: 'gold', fill: 0xff2d6a,
					fontSize: TEXTE_TAILLE,
					fontWeight: 'bold',
				}}
			/>
		</Container>
	</MainContainer>

	<PressToContinue decalageY={TAP_DECALAGE} onpress={() => oncomplete()} />
</FadeContainer>
