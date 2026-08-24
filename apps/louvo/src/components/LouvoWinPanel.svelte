<script lang="ts">
	import { onMount } from 'svelte';
	import { MainContainer } from 'components-layout';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { BitmapText, Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { counterAnchor } from '../game/boardBox';

	const context = getContext();

	// ============================================================
	// LE GAIN DU TOUR, SOUS LA GRILLE
	//
	// En dessous de BIG WIN, le montant s'affiche au centre de la
	// grille puis disparait quasi immediatement : Win.svelte appelle
	// finishCountUp() puis oncomplete() dans la foulee. En turbo, on
	// ne le voit pas. Ici il RESTE jusqu'au tour suivant.
	//
	// EN BASE GAME SEULEMENT. En bonus, cette bande porte deja le
	// compteur de free spins a gauche et le gain total a droite ;
	// entre les deux il reste 0,47 SYMBOL_SIZE et ce cadre en fait
	// 1,50. Le compteur TOTAL WIN y joue deja ce role.
	//
	// Le fondu ne joue QU'A LA DISPARITION : le montant surgit d'un
	// coup avec le gain, et s'efface doucement au tour suivant.
	// FadeContainer fait forcement les deux sens, d'ou le Container
	// simple et l'opacite pilotee ici - meme mecanique que les coeurs
	// de l'anticipation.
	// ============================================================
	const HAUTEUR = SYMBOL_SIZE * 1.0; // <<< LA taille du cadre
	const DECALAGE_Y = -SYMBOL_SIZE * 0.08; // <<< remonter (negatif) ou descendre
	const RATIO = 1536 / 1024; // proportions de votre image, a ne pas deformer
	const TEXTE_TAILLE = SYMBOL_SIZE * 0.26;
	const TEXTE_Y = 0; // le montant dans le cadre
	const SORTIE_MS = 320; // duree du fondu de disparition

	const largeur = HAUTEUR * RATIO;
	const ancre = $derived(counterAnchor(context.stateGame.tier));

	let montant = $state(0);
	let opacite = $state(0);

	let image: number | null = null;
	const arreter = () => {
		if (image !== null) {
			cancelAnimationFrame(image);
			image = null;
		}
	};

	// Apparition : franche, sans fondu.
	const apparaitre = () => {
		arreter();
		opacite = 1;
	};

	// Disparition : fondu, puis le composant se retire de lui-meme.
	const disparaitre = () => {
		arreter();
		if (opacite === 0) return;
		const depart = opacite;
		const debut = performance.now();
		const boucle = (maintenant: number) => {
			const t = (maintenant - debut) / SORTIE_MS;
			if (t >= 1) {
				opacite = 0;
				image = null;
				return;
			}
			opacite = depart * (1 - t);
			image = requestAnimationFrame(boucle);
		};
		image = requestAnimationFrame(boucle);
	};

	onMount(() => arreter);

	context.eventEmitter.subscribeOnMount({
		// Le tour suivant efface le montant du precedent.
		spinStart: () => disparaitre(),
		winUpdate: (emitterEvent) => {
			// Un gain tombe pendant un bonus ne doit pas etre memorise :
			// il reapparaitrait au retour en base game.
			if (context.stateGame.gameType !== 'basegame') return;
			if (emitterEvent.amount > 0) {
				montant = emitterEvent.amount;
				apparaitre();
			}
		},
	});

	const visible = $derived(opacite > 0 && context.stateGame.gameType === 'basegame');
</script>

<MainContainer>
	{#if visible}
		<Container
			x={ancre.centerX}
			y={ancre.y + HAUTEUR * 0.5 + DECALAGE_Y}
			alpha={opacite}
		>
			<Sprite anchor={0.5} key="totalWinFrame" width={largeur} height={HAUTEUR} />
			<BitmapText
				anchor={{ x: 0.5, y: 0.5 }}
				y={TEXTE_Y}
				text={bookEventAmountToCurrencyString(montant)}
				style={{
					fontFamily: 'gold', fill: 0xffffff,
					fontSize: TEXTE_TAILLE,
					wordWrap: false,
				}}
			/>
		</Container>
	{/if}
</MainContainer>
