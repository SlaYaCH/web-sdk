<script lang="ts">
	import { Container, Sprite, Rectangle, Text } from 'pixi-svelte';
	import { stateBet, stateModal } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';

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
		{ key: 'date', confirmKey: 'date', modeKey: 'MATCH_BOOST', desc: 'Chance x5 de bonus', mult: 3.0 },
		{ key: 'match', confirmKey: 'match', modeKey: 'MATCH_FRENZY', desc: 'Garantit des MATCH', mult: 60.0 },
		{ key: 'superlike', confirmKey: 'superlike', modeKey: 'LIKE_STORM', desc: 'Garantit un Super Like', mult: 60.0 },
		{ key: 'speeddating', confirmKey: 'speeddating', modeKey: 'BONUS_SPEED_DATING', desc: '10 tours - Speed Dating', mult: 80.0 },
		{ key: 'afterdark', confirmKey: 'afterdark', modeKey: 'BONUS_AFTER_DARK', desc: '10 tours - After Dark', mult: 150.0 },
	];

	let confirming = $state<(typeof OPTIONS)[number] | null>(null);

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
	const RETOUR_X = 0.2455 * CONFIRM_WIDTH - CONFIRM_WIDTH / 2;
	const OK_X = 0.633 * CONFIRM_WIDTH - CONFIRM_WIDTH / 2;
	const BUTTONS_Y = 0.871 * CONFIRM_HEIGHT - CONFIRM_HEIGHT / 2;
</script>

<Container>
	{#if !confirming}
		{#each OPTIONS as option, i}
			<Container
				x={(i - 2) * (CARD_WIDTH + CARD_GAP)}
				eventMode="static"
				cursor="pointer"
				onpointerup={() => onSelect(option)}
			>
				<Sprite key={`louvoCard_${option.key}`} anchor={0.5} width={CARD_WIDTH} height={CARD_HEIGHT} />
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
		<Container x={RETOUR_X} y={BUTTONS_Y} eventMode="static" cursor="pointer" onpointerup={onCancel}>
			<Rectangle anchor={0.5} width={100} height={40} alpha={0.001} backgroundColor={0x000000} />
		</Container>
		<Container x={OK_X} y={BUTTONS_Y} eventMode="static" cursor="pointer" onpointerup={onConfirm}>
			<Rectangle anchor={0.5} width={100} height={40} alpha={0.001} backgroundColor={0x000000} />
		</Container>
	{/if}
</Container>
