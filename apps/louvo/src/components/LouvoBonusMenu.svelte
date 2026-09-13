<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut, elasticOut } from 'svelte/easing';
	import { Container, Sprite, Rectangle, Text } from 'pixi-svelte';
	import { stateBet, stateModal } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import LouvoPressFx from './LouvoPressFx.svelte';

	const context = getContext();

	type Props = { onclose?: () => void };
	const props: Props = $props();

	// Mesures reelles sur les cartes (1024x1536) : cadre de texte du bas
	// x:110-910, y:1100-1360 - description et prix places dedans.
	const CARD_WIDTH = 170;
	const CARD_HEIGHT = 255;
	const CARD_GAP = 16;
	const DESC_Y = 0.755 * CARD_HEIGHT - CARD_HEIGHT / 2;
	const PRICE_Y = 0.846 * CARD_HEIGHT - CARD_HEIGHT / 2;
	const TEXT_WRAP_WIDTH = CARD_WIDTH * 0.78;

	const OPTIONS = [
		{ key: 'date', confirmKey: 'date', modeKey: 'MATCH_BOOST', desc: '5x bonus chance', mult: 3.0 },
		{ key: 'match', confirmKey: 'match', modeKey: 'MATCH_FRENZY', desc: 'Guaranteed MATCH', mult: 60.0 },
		{ key: 'superlike', confirmKey: 'superlike', modeKey: 'LIKE_STORM', desc: 'Guaranteed Super Like', mult: 60.0 },
		{ key: 'speeddating', confirmKey: 'speeddating', modeKey: 'BONUS_SPEED_DATING', desc: '10 spins - Speed Dating', mult: 80.0 },
		{ key: 'afterdark', confirmKey: 'afterdark', modeKey: 'BONUS_AFTER_DARK', desc: '10 spins - After Dark', mult: 150.0 },
	];

	let confirming = $state<(typeof OPTIONS)[number] | null>(null);

	// ============================================================
	// LE GESTE DU CLIC                                  (lot 137)
	//
	// Deux cas differents dans cet ecran :
	//
	//   LES CARTES sont de vrais sprites. Elles se soulevent au
	//   survol, s'enfoncent sous le doigt, reviennent en rebond.
	//   Le voile de l'appui est DEDUIT de l'echelle : pas de
	//   minuterie en plus, il suit le meme mouvement.
	//
	//   LES BOUTONS RETOUR ET OK sont peints DANS l'image de
	//   confirmation - deux rectangles invisibles par-dessus,
	//   comme la barre du bas. Le geste s'y joue en surimpression,
	//   par LouvoPressFx.
	//
	// Pas d'onde sur RETOUR et OK : onConfirm fait disparaitre
	// l'ecran dans la milliseconde, elle n'aurait pas une seule
	// image pour s'afficher. On ne cable pas ce qui ne se voit pas.
	//
	// Aucun gestionnaire n'est modifie.
	// ============================================================
	const CARTE_SURVOL = 1.05; // de combien elle grandit au survol
	const CARTE_APPUI = 0.94; // de combien elle s'enfonce
	const CARTE_LEVEE = -120; // la levee : (echelle - 1) x ceci
	const CARTE_VOILE = 3; // l'assombrissement a l'appui

	const survolCarte = $state(OPTIONS.map(() => false));
	const appuiCarte = $state(OPTIONS.map(() => false));
	const echelleCarte = OPTIONS.map(
		() => new Tween(1, { duration: 200, easing: cubicOut }),
	);
	$effect(() => {
		OPTIONS.forEach((_option, i) => {
			const presse = appuiCarte[i];
			echelleCarte[i].set(
				presse ? CARTE_APPUI : survolCarte[i] ? CARTE_SURVOL : 1,
				presse
					? { duration: 60, easing: cubicOut }
					: { duration: 240, easing: elasticOut },
			);
		});
	});

	const survolConfirm = $state({ retour: false, ok: false });
	const appuiConfirm = $state({ retour: false, ok: false });

	const priceFor = (mult: number) => numberToCurrencyString(stateBet.betAmount * mult);

	const onSelect = (option: (typeof OPTIONS)[number]) => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		confirming = option;
	};
	const onCancel = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		confirming = null;
	};
	const onConfirm = () => {
		if (!confirming) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const isBuyMode =
			confirming.modeKey === 'BONUS_SPEED_DATING' || confirming.modeKey === 'BONUS_AFTER_DARK';
		stateBet.activeBetModeKey = confirming.modeKey;
		confirming = null;
		stateModal.modal = null;
		// L'affichage du menu est pilote par une variable locale de Game.svelte,
		// pas par stateModal : sans ce rappel, l'ecran de selection se rouvre.
		props.onclose?.();
		// Les modes "achat" doivent lancer le tour tout de suite (les modes
		// "activation" attendent que le joueur appuie sur SPIN lui-meme).
		if (isBuyMode) {
			context.eventEmitter.broadcast({ type: 'bet' });
		}
	};

	// Mesures reelles sur les fenetres de confirmation (1161x1355)
	const CONFIRM_WIDTH = 320;
	const CONFIRM_HEIGHT = 374;
	const CONFIRM_DESC_Y = 0.6494 * CONFIRM_HEIGHT - CONFIRM_HEIGHT / 2;
	// ============================================================
	// LES BOUTONS DES CONFIRMATIONS                     (lot 138)
	//
	// Mesures relevees dans chacune des cinq images sources, puis
	// verifiees en superposition. Les cinq fenetres n'ont PAS leurs
	// boutons au meme endroit ni a la meme taille : un seul jeu de
	// constantes (c'etait 0.2455 / 0.633 / 0.871) ne pouvait tomber
	// juste nulle part - jusqu'a 23 px d'ecart sur 320.
	//
	// Ce sont des fractions de la largeur / hauteur de CHAQUE image,
	// donc justes quel que soit l'etirement au rendu.
	// ============================================================
	const BOUTONS_CONFIRM = {
		match: { back: 0.315, ok: 0.695, y: 0.882, l: 0.32, h: 0.078 },
		superlike: { back: 0.315, ok: 0.66, y: 0.844, l: 0.28, h: 0.065 },
		date: { back: 0.332, ok: 0.681, y: 0.894, l: 0.322, h: 0.082 },
		speeddating: { back: 0.31, ok: 0.695, y: 0.9085, l: 0.27, h: 0.067 },
		afterdark: { back: 0.31, ok: 0.695, y: 0.919, l: 0.27, h: 0.067 },
	} as const;

	// La zone cliquable deborde un peu du bouton peint : plus facile
	// a viser, surtout au doigt.
	const ZONE_MARGE = 14;

	const boutons = $derived(
		BOUTONS_CONFIRM[
			(confirming?.confirmKey ?? 'match') as keyof typeof BOUTONS_CONFIRM
		],
	);
	const RETOUR_X = $derived(boutons.back * CONFIRM_WIDTH - CONFIRM_WIDTH / 2);
	const OK_X = $derived(boutons.ok * CONFIRM_WIDTH - CONFIRM_WIDTH / 2);
	const BUTTONS_Y = $derived(boutons.y * CONFIRM_HEIGHT - CONFIRM_HEIGHT / 2);
	const BOUTON_L = $derived(boutons.l * CONFIRM_WIDTH);
	const BOUTON_H = $derived(boutons.h * CONFIRM_HEIGHT);
</script>

<Container>
	{#if !confirming}
		{#each OPTIONS as option, i}
			<Container
				x={(i - 2) * (CARD_WIDTH + CARD_GAP)}
				y={(echelleCarte[i].current - 1) * CARTE_LEVEE}
				scale={echelleCarte[i].current}
				eventMode="static"
				cursor="pointer"
				onpointerover={() => (survolCarte[i] = true)}
				onpointerout={() => {
					survolCarte[i] = false;
					appuiCarte[i] = false;
				}}
				onpointerdown={() => (appuiCarte[i] = true)}
				onpointerup={() => {
					appuiCarte[i] = false;
					onSelect(option);
				}}
			>
				<Sprite key={`louvoCard_${option.key}`} anchor={0.5} width={CARD_WIDTH} height={CARD_HEIGHT} />
				<!-- Le voile de l'appui, deduit de l'echelle : il suit le
				     meme mouvement, sans minuterie ni etat en plus. -->
				<Rectangle
					anchor={0.5}
					width={CARD_WIDTH}
					height={CARD_HEIGHT}
					backgroundColor={0x000000}
					alpha={Math.max(0, (1 - echelleCarte[i].current) * CARTE_VOILE)}
				/>
				<Text
					anchor={0.5}
					y={DESC_Y}
					text={option.desc}
					style={{
						fontFamily: 'proxima-nova',
						fontWeight: '600',
						fontSize: 11,
						fill: 0xffffff,
						align: 'center',
						wordWrap: true,
						wordWrapWidth: TEXT_WRAP_WIDTH,
					}}
				/>
				<Text
					anchor={0.5}
					y={PRICE_Y}
					text={priceFor(option.mult)}
					style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 15, fill: 0xffffff }}
				/>
			</Container>
		{/each}
	{:else}
		{@const isDateStack = confirming.confirmKey === 'speeddating' || confirming.confirmKey === 'afterdark'}
		<Sprite key={`louvoConfirm_${confirming.confirmKey}`} anchor={0.5} width={CONFIRM_WIDTH} height={CONFIRM_HEIGHT} />
		<Text
			anchor={0.5}
			y={isDateStack ? 0.8 * CONFIRM_HEIGHT - CONFIRM_HEIGHT / 2 : CONFIRM_DESC_Y}
			text={`${confirming.desc} — ${priceFor(confirming.mult)}`}
			style={{
				fontFamily: 'proxima-nova',
				fontWeight: '600',
				fontSize: 16,
				fill: 0xffffff,
				align: 'center',
				wordWrap: true,
				wordWrapWidth: CONFIRM_WIDTH - 50,
			}}
		/>
		<Container
			x={RETOUR_X}
			y={BUTTONS_Y}
			eventMode="static"
			cursor="pointer"
			onpointerover={() => (survolConfirm.retour = true)}
			onpointerout={() => {
				survolConfirm.retour = false;
				appuiConfirm.retour = false;
			}}
			onpointerdown={() => (appuiConfirm.retour = true)}
			onpointerup={() => {
				appuiConfirm.retour = false;
				onCancel();
			}}
		>
			<Rectangle
				anchor={0.5}
				width={BOUTON_L + ZONE_MARGE}
				height={BOUTON_H + ZONE_MARGE}
				alpha={0.001}
				backgroundColor={0x000000}
			/>
			<LouvoPressFx
				largeur={BOUTON_L}
				hauteur={BOUTON_H}
				survole={survolConfirm.retour}
				presse={appuiConfirm.retour}
			/>
		</Container>
		<Container
			x={OK_X}
			y={BUTTONS_Y}
			eventMode="static"
			cursor="pointer"
			onpointerover={() => (survolConfirm.ok = true)}
			onpointerout={() => {
				survolConfirm.ok = false;
				appuiConfirm.ok = false;
			}}
			onpointerdown={() => (appuiConfirm.ok = true)}
			onpointerup={() => {
				appuiConfirm.ok = false;
				onConfirm();
			}}
		>
			<Rectangle
				anchor={0.5}
				width={BOUTON_L + ZONE_MARGE}
				height={BOUTON_H + ZONE_MARGE}
				alpha={0.001}
				backgroundColor={0x000000}
			/>
			<LouvoPressFx
				largeur={BOUTON_L}
				hauteur={BOUTON_H}
				survole={survolConfirm.ok}
				presse={appuiConfirm.ok}
			/>
		</Container>
	{/if}
</Container>
