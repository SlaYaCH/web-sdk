<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { Container, Sprite, Text, Rectangle } from 'pixi-svelte';
	import { stateBet, stateBetDerived, stateConfig, stateUi, stateModal } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';
	import { OnHotkey } from 'components-shared';

	import { getContext } from '../game/context';

	const context = getContext();

	// ============================================================
	// Mesures reelles sur l'asset (louvo_bottom_bar.png) - en
	// fractions de la largeur/hauteur, valables quelle que soit la
	// taille de rendu choisie ci-dessous.
	// ============================================================
	const BAR_WIDTH = 1300;
	const BAR_HEIGHT = 240;
	const ROW_Y = BAR_HEIGHT * 0.511 - BAR_HEIGHT / 2;

	const BONUS_X = -BAR_WIDTH / 2 - 45; // juste a gauche de la barre, reste dans le cadre visible
	const MENU_X = BAR_WIDTH * 0.116 - BAR_WIDTH / 2;
	const BALANCE_X = BAR_WIDTH * 0.331 - BAR_WIDTH / 2;
	const STEPPER_ARROWS_X = BAR_WIDTH * 0.623 - BAR_WIDTH / 2;
	const STEPPER_SLOT_X = BAR_WIDTH * 0.686 - BAR_WIDTH / 2;
	const SPIN_X = BAR_WIDTH * 0.881 - BAR_WIDTH / 2;
	const AUTOSPIN_X = BAR_WIDTH * 0.970 - BAR_WIDTH / 2;

	// --- Solde (tween, comme LabelBalance.svelte) ---
	const balanceTween = new Tween(stateBet.balanceAmount);
	$effect(() => {
		balanceTween.set(stateBet.balanceAmount);
	});
	const balanceText = $derived(numberToCurrencyString(balanceTween.current));

	// --- Mise actuelle ---
	const betText = $derived(numberToCurrencyString(stateBetDerived.betCost()));

	// --- Stepper mise (logique identique a ButtonIncrease/ButtonDecrease) ---
	const biggestBet = $derived(stateConfig.betAmountOptions[stateConfig.betAmountOptions.length - 1]);
	const smallestBet = $derived(stateConfig.betAmountOptions[0]);
	const increaseDisabled = $derived(
		!context.stateXstateDerived.isIdle() || stateBet.betAmount === biggestBet,
	);
	const decreaseDisabled = $derived(
		!context.stateXstateDerived.isIdle() || stateBet.betAmount === smallestBet,
	);

	const onIncrease = () => {
		if (increaseDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const nextBigger = [...stateConfig.betAmountOptions]
			.sort((a, b) => a - b)
			.find((option) => option > stateBet.betAmount);
		stateBetDerived.setBetAmount(nextBigger || biggestBet);
	};
	const onDecrease = () => {
		if (decreaseDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const nextSmaller = [...stateConfig.betAmountOptions]
			.sort((a, b) => b - a)
			.find((option) => option < stateBet.betAmount);
		stateBetDerived.setBetAmount(nextSmaller || smallestBet);
	};

	// --- Menu (identique a ButtonMenu.svelte) ---
	const onMenu = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateUi.menuOpen = true;
	};

	// --- Bonus (logique identique a ButtonBuyBonus.svelte reel) ---
	const bonusActive = $derived(stateBetDerived.activeBetMode()?.type === 'activate');
	const bonusDisabled = $derived(!context.stateXstateDerived.isIdle());
	const onBonus = () => {
		if (bonusDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (bonusActive) {
			stateBet.activeBetModeKey = 'BASE';
		} else {
			context.eventEmitter.broadcast({ type: 'bonusMenuShow' });
		}
	};

	// --- Autoplay (identique a ButtonAutoSpin.svelte, compteur simplifie) ---
	const hasAutoBetCounter = $derived(stateBetDerived.hasAutoBetCounter());
	const autoSpinDisabled = $derived.by(() => {
		if (stateBet.isSpaceHold) return true;
		if (!context.stateXstateDerived.isIdle() && !stateBetDerived.hasAutoBetCounter()) return true;
		if (!stateBetDerived.isBetCostAvailable()) return true;
		return false;
	});
	const onAutoSpin = () => {
		if (autoSpinDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (hasAutoBetCounter) {
			stateBet.autoSpinsCounter = 0;
		} else {
			stateModal.modal = { name: 'autoSpin' };
		}
	};

	// --- Spin / Stop (logique reprise directement de ButtonBetProvider.svelte,
	// qui n'est pas exporte publiquement par components-ui-pixi) ---
	let stopDisabled = $state(false);
	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => (stopDisabled = true),
		stopButtonEnable: () => (stopDisabled = false),
	});
	const spinDisabled = $derived.by(() => {
		if (context.stateXstateDerived.isIdle()) {
			return !stateBetDerived.isBetCostAvailable();
		}
		if (stopDisabled) return true;
		if (!stateBetDerived.hasAutoBetCounter() && stateBet.isTurbo) return true;
		return false;
	});
	const onSpinPress = () => {
		context.eventEmitter.broadcast({ type: 'soundPressBet' });
		if (context.stateXstateDerived.isIdle()) {
			if (stateBetDerived.activeBetMode()?.type === 'buy') stateBet.activeBetModeKey = 'BASE';
			context.eventEmitter.broadcast({ type: 'bet' });
		} else if (!stopDisabled) {
			if (stateBetDerived.hasAutoBetCounter()) stateBet.autoSpinsCounter = 0;
			context.eventEmitter.broadcast({ type: 'stopButtonClick' });
		}
	};
</script>

<Container x={0} y={-BAR_HEIGHT * 0.5}>
	<Sprite key="uiBottomBar" anchor={0.5} width={BAR_WIDTH} height={BAR_HEIGHT} />

	<!-- Bonus -->
	<Container
		x={BONUS_X}
		y={ROW_Y}
		eventMode={bonusDisabled ? 'none' : 'static'}
		cursor={bonusDisabled ? 'not-allowed' : 'pointer'}
		alpha={bonusDisabled ? 0.5 : 1}
		onpointerup={onBonus}
	>
		<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
		{#if bonusActive}
			<Rectangle anchor={0.5} width={90} height={90} alpha={0} borderColor={0xffffff} borderWidth={4} />
		{/if}
	</Container>

	<!-- Menu -->
	<Container
		x={MENU_X}
		y={ROW_Y}
		eventMode="static"
		cursor="pointer"
		onpointerup={onMenu}
	>
		<Rectangle anchor={0.5} width={100} height={100} alpha={0.001} backgroundColor={0x000000} />
	</Container>

	<!-- Solde -->
	<Text
		x={BALANCE_X}
		y={ROW_Y}
		anchor={0.5}
		text={balanceText}
		style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 32, fill: 0xffffff }}
	/>

	<!-- Mise (case) -->
	<Text
		x={STEPPER_SLOT_X}
		y={ROW_Y}
		anchor={0.5}
		text={betText}
		style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 26, fill: 0xffffff }}
	/>

	<!-- Fleche haut (augmenter) -->
	<Container
		x={STEPPER_ARROWS_X}
		y={ROW_Y - 22}
		eventMode={increaseDisabled ? 'none' : 'static'}
		cursor={increaseDisabled ? 'not-allowed' : 'pointer'}
		alpha={increaseDisabled ? 0.4 : 1}
		onpointerup={onIncrease}
	>
		<Rectangle anchor={0.5} width={50} height={40} alpha={0.001} backgroundColor={0x000000} />
	</Container>

	<!-- Fleche bas (diminuer) -->
	<Container
		x={STEPPER_ARROWS_X}
		y={ROW_Y + 22}
		eventMode={decreaseDisabled ? 'none' : 'static'}
		cursor={decreaseDisabled ? 'not-allowed' : 'pointer'}
		alpha={decreaseDisabled ? 0.4 : 1}
		onpointerup={onDecrease}
	>
		<Rectangle anchor={0.5} width={50} height={40} alpha={0.001} backgroundColor={0x000000} />
	</Container>

	<!-- Autoplay -->
	<Container
		x={AUTOSPIN_X}
		y={ROW_Y}
		eventMode={autoSpinDisabled ? 'none' : 'static'}
		cursor={autoSpinDisabled ? 'not-allowed' : 'pointer'}
		onpointerup={onAutoSpin}
	>
		<Rectangle anchor={0.5} width={70} height={70} alpha={0.001} backgroundColor={0x000000} />
		{#if hasAutoBetCounter}
			<Text
				anchor={0.5}
				y={-55}
				text={String(stateBet.autoSpinsCounter)}
				style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 24, fill: 0xffffff }}
			/>
		{/if}
	</Container>

	<!-- Spin / Stop -->
	<OnHotkey hotkey="Space" disabled={spinDisabled} onpress={onSpinPress} />
	<Container
		x={SPIN_X}
		y={ROW_Y}
		eventMode={spinDisabled ? 'none' : 'static'}
		cursor={spinDisabled ? 'not-allowed' : 'pointer'}
		onpointerup={onSpinPress}
	>
		<Rectangle anchor={0.5} width={180} height={180} alpha={0.001} backgroundColor={0x000000} />
	</Container>
</Container>
