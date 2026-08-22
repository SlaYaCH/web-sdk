<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { stateBet, stateUi } from 'state-shared';
	import { API_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';

	const context = getContext();

	const BAR_WIDTH = 1300;
	const BAR_HEIGHT = 150;

	// Meme raison que dans LouvoBottomBar : 1300 de large ne rentre pas
	// dans les 1080 de la mise en page standard en portrait.
	const barScale = $derived(
		Math.min(1, (context.stateLayoutDerived.mainLayoutStandard().width - 40) / BAR_WIDTH),
	);

	const LABEL = {
		fontFamily: 'proxima-nova',
		fontWeight: '600',
		fontSize: 18,
		fill: 0xff8fb3,
	} as const;
	const VALUE = {
		fontFamily: 'proxima-nova',
		fontWeight: '700',
		fontSize: 30,
		fill: 0xffffff,
	} as const;
	const BUTTON = {
		fontFamily: 'proxima-nova',
		fontWeight: '700',
		fontSize: 22,
		fill: 0xffffff,
	} as const;

	// ------------------------------------------------------------------
	// Les donnees du replay arrivent dans stateBet.betToResume, pose par
	// Authenticate.svelte apres GET /bet/replay/{game}/{version}/{mode}/{event}.
	// ResumeBet.svelte les consomme ensuite, donc on les capture des qu'elles
	// apparaissent au lieu de lire betToResume en continu.
	// ------------------------------------------------------------------
	type ReplayRound = {
		amount?: number;
		payout?: number;
		payoutMultiplier?: number;
	};

	let seenRound = $state(false);
	let payout = $state<number | null>(null);
	let payoutMultiplier = $state<number | null>(null);
	let timedOut = $state(false);

	$effect(() => {
		const round = stateBet.betToResume as unknown as ReplayRound | null;
		if (!round || seenRound) return;
		seenRound = true;
		if (typeof round.payout === 'number') payout = round.payout;
		if (typeof round.payoutMultiplier === 'number') payoutMultiplier = round.payoutMultiplier;
	});

	// Event ID invalide : le RGS ne renvoie pas de round, on le dit clairement
	// au lieu de laisser un ecran fige.
	onMount(() => {
		const timer = setTimeout(() => {
			if (!seenRound) timedOut = true;
		}, 6000);
		return () => clearTimeout(timer);
	});

	const betText = $derived(numberToCurrencyString(stateBet.betAmount));
	const winText = $derived(
		payout === null ? '-' : numberToCurrencyString(payout / API_AMOUNT_MULTIPLIER),
	);
	const multiplierText = $derived.by(() => {
		if (payoutMultiplier !== null) return `${payoutMultiplier.toFixed(2)}x`;
		if (payout !== null && stateBet.betAmount > 0)
			return `${(payout / API_AMOUNT_MULTIPLIER / stateBet.betAmount).toFixed(2)}x`;
		return '-';
	});

	// Rejouer le meme event : on recharge l'URL telle quelle, elle contient
	// deja replay=true et l'event. Aucune mise n'est envoyee.
	const onReplayAgain = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (typeof window !== 'undefined') window.location.reload();
	};

	const onMenu = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateUi.menuOpen = true;
	};

	const COL_MENU = -BAR_WIDTH * 0.5 + 110;
	const COL_BET = -BAR_WIDTH * 0.5 + 330;
	const COL_WIN = -BAR_WIDTH * 0.5 + 560;
	const COL_MULT = -BAR_WIDTH * 0.5 + 790;
	const COL_BUTTON = BAR_WIDTH * 0.5 - 190;
</script>

<Container x={0} y={-BAR_HEIGHT * 0.5 * barScale} scale={barScale}>
	<Rectangle
		anchor={0.5}
		width={BAR_WIDTH}
		height={BAR_HEIGHT}
		backgroundColor={0x1a0a14}
		borderColor={0xff2d6a}
		borderWidth={4}
	/>

	<!-- Bandeau : on est en relecture, pas en jeu -->
	<Text
		x={-BAR_WIDTH * 0.5 + 110}
		y={-BAR_HEIGHT * 0.5 + 26}
		anchor={0.5}
		text="REPLAY"
		style={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 20, fill: 0xff2d6a }}
	/>

	{#if timedOut}
		<Text
			anchor={0.5}
			text="REPLAY UNAVAILABLE - CHECK THE EVENT ID"
			style={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 26, fill: 0xff2d6a }}
		/>
	{:else}
		<!-- MENU -->
		<Container x={COL_MENU} y={22} eventMode="static" cursor="pointer" onpointerup={onMenu}>
			<Rectangle
				anchor={0.5}
				width={150}
				height={52}
				backgroundColor={0x330018}
				borderColor={0xff2d6a}
				borderWidth={2}
			/>
			<Text anchor={0.5} text="MENU" style={BUTTON} />
		</Container>

		<!-- BET -->
		<Text x={COL_BET} y={-18} anchor={0.5} text="BET" style={LABEL} />
		<Text x={COL_BET} y={20} anchor={0.5} text={betText} style={VALUE} />

		<!-- WIN -->
		<Text x={COL_WIN} y={-18} anchor={0.5} text="WIN" style={LABEL} />
		<Text x={COL_WIN} y={20} anchor={0.5} text={winText} style={VALUE} />

		<!-- MULTIPLIER -->
		<Text x={COL_MULT} y={-18} anchor={0.5} text="MULTIPLIER" style={LABEL} />
		<Text x={COL_MULT} y={20} anchor={0.5} text={multiplierText} style={VALUE} />

		<!-- REPLAY AGAIN -->
		<Container x={COL_BUTTON} eventMode="static" cursor="pointer" onpointerup={onReplayAgain}>
			<Rectangle
				anchor={0.5}
				width={280}
				height={62}
				backgroundColor={0x330018}
				borderColor={0xff2d6a}
				borderWidth={2}
			/>
			<Text anchor={0.5} text="REPLAY AGAIN" style={BUTTON} />
		</Container>
	{/if}
</Container>
