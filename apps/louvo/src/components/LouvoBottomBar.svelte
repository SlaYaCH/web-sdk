<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut, elasticOut } from 'svelte/easing';
	import { Container, Sprite, Text, Rectangle } from 'pixi-svelte';
	import { stateBet, stateBetDerived, stateConfig, stateUi, stateModal } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';
	import { OnHotkey } from 'components-shared';

	import { getContext } from '../game/context';
	import LouvoPressFx from './LouvoPressFx.svelte';

	const context = getContext();

	// ============================================================
	// LE GESTE DU CLIC                                  (lot 136)
	//
	// Les boutons sont peints dans bottom_bar.webp : il n'y a aucun
	// sprite a enfoncer. Le geste se joue en surimpression, par
	// LouvoPressFx, pose DANS chaque zone cliquable. Au repos tout
	// est a alpha 0 : le visuel est intact.
	//
	// survol / appui : ce que fait la souris.
	// coups          : incremente DANS le gestionnaire, apres les
	//                  garde-fous. Donc la barre Espace anime le
	//                  bouton aussi, et un bouton eteint ne
	//                  clignote pas pour rien.
	// ============================================================
	const survol = $state({
		bonus: false,
		menu: false,
		haut: false,
		bas: false,
		auto: false,
		spin: false,
	});
	const appui = $state({
		bonus: false,
		menu: false,
		haut: false,
		bas: false,
		auto: false,
		spin: false,
	});
	const coups = $state({
		bonus: 0,
		menu: 0,
		haut: 0,
		bas: 0,
		auto: 0,
		spin: 0,
	});

	// Le BONUS a un vrai sprite : lui peut s'enfoncer pour de bon.
	const bonusEchelle = new Tween(1, { duration: 70, easing: cubicOut });
	$effect(() => {
		bonusEchelle.set(
			appui.bonus ? 0.93 : 1,
			appui.bonus ? { duration: 70, easing: cubicOut }
				: { duration: 260, easing: elasticOut },
		);
	});

	// ============================================================
	// Mesures reelles sur l'asset (louvo_bottom_bar.png) - en
	// fractions de la largeur/hauteur, valables quelle que soit la
	// taille de rendu choisie ci-dessous.
	// ============================================================
	const BAR_WIDTH = 1300;
	const BAR_HEIGHT = 240;
	const ROW_Y = BAR_HEIGHT * 0.511 - BAR_HEIGHT / 2;

	// En portrait la mise en page standard ne fait que 1080 de large :
	// une barre de 1300 serait coupee des deux cotes. Plafonne a 1, donc
	// aucun changement sur desktop (1920 de large).
	const barScale = $derived(
		Math.min(1, (context.stateLayoutDerived.mainLayoutStandard().width - 40) / BAR_WIDTH),
	);

	// Le BONUS est pose AU-DESSUS du bouton 3 traits : meme colonne que
	// MENU_X, remonte au-dessus de la barre. Il debordait a gauche avant,
	// et sortait de l'ecran sur petit format.
	const BONUS_X = BAR_WIDTH * 0.116 - BAR_WIDTH / 2;
	const BONUS_Y_OFFSET = -118;

	// ============================================================
	// LES POSITIONS, MESUREES DANS bottom_bar.webp      (lot 138)
	//
	// L'image fait 1486 x 274 et se rend en 1300 x 240 : les
	// fractions ci-dessous se transposent telles quelles.
	//
	// Les zones cliquables etaient decalees DEPUIS LE DEBUT. On ne
	// le voyait pas tant qu'aucun effet ne les dessinait :
	//     SPIN      25 px trop a droite, 16 px trop bas
	//     AUTOPLAY   5 px trop a droite, 19 px trop haut
	//     fleches    6 px trop a droite, ecartees de 44 au lieu de 23
	//
	// ROW_Y n'est PAS touche : il sert aussi au solde et a la mise,
	// qui ne doivent pas bouger. Chaque bouton a son propre y.
	// ============================================================
	const MENU_X = BAR_WIDTH * 0.1134 - BAR_WIDTH / 2;
	const MENU_Y = BAR_HEIGHT * 0.5157 - BAR_HEIGHT / 2;
	const BALANCE_X = BAR_WIDTH * 0.331 - BAR_WIDTH / 2;
	const STEPPER_ARROWS_X = BAR_WIDTH * 0.6181 - BAR_WIDTH / 2;
	const HAUT_Y = BAR_HEIGHT * 0.4843 - BAR_HEIGHT / 2;
	const BAS_Y = BAR_HEIGHT * 0.581 - BAR_HEIGHT / 2;
	const STEPPER_SLOT_X = BAR_WIDTH * 0.686 - BAR_WIDTH / 2;
	const SPIN_X = BAR_WIDTH * 0.8614 - BAR_WIDTH / 2;
	const SPIN_Y = BAR_HEIGHT * 0.4453 - BAR_HEIGHT / 2;
	const AUTOSPIN_X = BAR_WIDTH * 0.9665 - BAR_WIDTH / 2;
	const AUTOSPIN_Y = BAR_HEIGHT * 0.5912 - BAR_HEIGHT / 2;

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
		coups.haut += 1;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const nextBigger = [...stateConfig.betAmountOptions]
			.sort((a, b) => a - b)
			.find((option) => option > stateBet.betAmount);
		stateBetDerived.setBetAmount(nextBigger || biggestBet);
	};
	const onDecrease = () => {
		if (decreaseDisabled) return;
		coups.bas += 1;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const nextSmaller = [...stateConfig.betAmountOptions]
			.sort((a, b) => b - a)
			.find((option) => option < stateBet.betAmount);
		stateBetDerived.setBetAmount(nextSmaller || smallestBet);
	};

	// --- Menu (identique a ButtonMenu.svelte) ---
	const onMenu = () => {
		coups.menu += 1;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateUi.menuOpen = true;
	};

	// --- Bonus (logique identique a ButtonBuyBonus.svelte reel) ---
	const bonusActive = $derived(stateBetDerived.activeBetMode()?.type === 'activate');
	const bonusDisabled = $derived(!context.stateXstateDerived.isIdle());
	const onBonus = () => {
		if (bonusDisabled) return;
		coups.bonus += 1;
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
		coups.auto += 1;
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
		coups.spin += 1;
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

<Container x={0} y={-BAR_HEIGHT * 0.5 * barScale} scale={barScale}>
	<Sprite key="uiBottomBar" anchor={0.5} width={BAR_WIDTH} height={BAR_HEIGHT} />

	<!-- Bonus -->
	<Container
		x={BONUS_X}
		y={ROW_Y + BONUS_Y_OFFSET}
		scale={bonusEchelle.current}
		eventMode={bonusDisabled ? 'none' : 'static'}
		cursor={bonusDisabled ? 'not-allowed' : 'pointer'}
		alpha={bonusDisabled ? 0.5 : 1}
		onpointerover={() => (survol.bonus = true)}
		onpointerout={() => {
			survol.bonus = false;
			appui.bonus = false;
		}}
		onpointerdown={() => (appui.bonus = true)}
		onpointerup={() => {
			appui.bonus = false;
			onBonus();
		}}
	>
		<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
		<LouvoPressFx
			largeur={90}
			hauteur={90}
			survole={survol.bonus}
			presse={appui.bonus}
			actif={!bonusDisabled}
			coup={coups.bonus}
			voileEteint={0}
		/>
		{#if bonusActive}
			<Rectangle anchor={0.5} width={90} height={90} backgroundColor={0x1a0a14} borderColor={0xff2d6a} borderWidth={4} />
			<Text
				anchor={0.5}
				text="OFF"
				style={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 24, fill: 0xffffff }}
			/>
		{/if}
	</Container>

	<!-- Menu -->
	<Container
		x={MENU_X}
		y={MENU_Y}
		eventMode="static"
		cursor="pointer"
		onpointerover={() => (survol.menu = true)}
		onpointerout={() => {
			survol.menu = false;
			appui.menu = false;
		}}
		onpointerdown={() => (appui.menu = true)}
		onpointerup={() => {
			appui.menu = false;
			onMenu();
		}}
	>
		<Rectangle anchor={0.5} width={126} height={92} alpha={0.001} backgroundColor={0x000000} />
		<LouvoPressFx
			largeur={121}
			hauteur={85}
			survole={survol.menu}
			presse={appui.menu}
			coup={coups.menu}
		/>
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
		y={HAUT_Y}
		eventMode={increaseDisabled ? 'none' : 'static'}
		cursor={increaseDisabled ? 'not-allowed' : 'pointer'}
		alpha={increaseDisabled ? 0.4 : 1}
		onpointerover={() => (survol.haut = true)}
		onpointerout={() => {
			survol.haut = false;
			appui.haut = false;
		}}
		onpointerdown={() => (appui.haut = true)}
		onpointerup={() => {
			appui.haut = false;
			onIncrease();
		}}
	>
		<Rectangle anchor={0.5} width={46} height={23} alpha={0.001} backgroundColor={0x000000} />
		<LouvoPressFx
			largeur={30}
			hauteur={22}
			survole={survol.haut}
			presse={appui.haut}
			actif={!increaseDisabled}
			coup={coups.haut}
			voileEteint={0}
		/>
	</Container>

	<!-- Fleche bas (diminuer) -->
	<Container
		x={STEPPER_ARROWS_X}
		y={BAS_Y}
		eventMode={decreaseDisabled ? 'none' : 'static'}
		cursor={decreaseDisabled ? 'not-allowed' : 'pointer'}
		alpha={decreaseDisabled ? 0.4 : 1}
		onpointerover={() => (survol.bas = true)}
		onpointerout={() => {
			survol.bas = false;
			appui.bas = false;
		}}
		onpointerdown={() => (appui.bas = true)}
		onpointerup={() => {
			appui.bas = false;
			onDecrease();
		}}
	>
		<Rectangle anchor={0.5} width={46} height={23} alpha={0.001} backgroundColor={0x000000} />
		<LouvoPressFx
			largeur={30}
			hauteur={22}
			survole={survol.bas}
			presse={appui.bas}
			actif={!decreaseDisabled}
			coup={coups.bas}
			voileEteint={0}
		/>
	</Container>

	<!-- Autoplay -->
	<Container
		x={AUTOSPIN_X}
		y={AUTOSPIN_Y}
		eventMode={autoSpinDisabled ? 'none' : 'static'}
		cursor={autoSpinDisabled ? 'not-allowed' : 'pointer'}
		onpointerover={() => (survol.auto = true)}
		onpointerout={() => {
			survol.auto = false;
			appui.auto = false;
		}}
		onpointerdown={() => (appui.auto = true)}
		onpointerup={() => {
			appui.auto = false;
			onAutoSpin();
		}}
	>
		<Rectangle anchor={0.5} width={70} height={70} alpha={0.001} backgroundColor={0x000000} />
		<LouvoPressFx
			largeur={60}
			hauteur={60}
			cercle={true}
			survole={survol.auto}
			presse={appui.auto}
			actif={!autoSpinDisabled}
			coup={coups.auto}
		/>
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
		y={SPIN_Y}
		eventMode={spinDisabled ? 'none' : 'static'}
		cursor={spinDisabled ? 'not-allowed' : 'pointer'}
		onpointerover={() => (survol.spin = true)}
		onpointerout={() => {
			survol.spin = false;
			appui.spin = false;
		}}
		onpointerdown={() => (appui.spin = true)}
		onpointerup={() => {
			appui.spin = false;
			onSpinPress();
		}}
	>
		<Rectangle anchor={0.5} width={180} height={180} alpha={0.001} backgroundColor={0x000000} />
		<LouvoPressFx
			largeur={162}
			hauteur={162}
			cercle={true}
			survole={survol.spin}
			presse={appui.spin}
			actif={!spinDisabled}
			coup={coups.spin}
		/>
	</Container>
</Container>
