<script lang="ts">
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { stateHistory, type HistoryRound } from '../game/stateHistory.svelte';
	import { playBet } from '../game/utils';

	type Props = { onclose: () => void };

	const props: Props = $props();
	const context = getContext();

	const PANEL_WIDTH = 980;
	const PANEL_HEIGHT = 640;
	const ROW_HEIGHT = 42;
	const ROW_GAP = 46;
	const VISIBLE_ROWS = 10;

	const HEAD = {
		fontFamily: 'proxima-nova',
		fontWeight: '700',
		fontSize: 17,
		fill: 0xff8fb3,
	} as const;
	const CELL = {
		fontFamily: 'proxima-nova',
		fontWeight: '600',
		fontSize: 19,
		fill: 0xffffff,
	} as const;

	// Colonnes, en x relatif au centre du panneau
	const COL = {
		time: -PANEL_WIDTH / 2 + 90,
		mode: -PANEL_WIDTH / 2 + 260,
		id: -PANEL_WIDTH / 2 + 470,
		bet: -PANEL_WIDTH / 2 + 640,
		win: -PANEL_WIDTH / 2 + 780,
		mult: -PANEL_WIDTH / 2 + 900,
	};

	const rows = $derived(stateHistory.rounds.slice(0, VISIBLE_ROWS));
	const canReplay = $derived(context.stateXstateDerived.isIdle());

	const TOP = -PANEL_HEIGHT / 2 + 96;

	// Relecture LOCALE du tour deja stocke : aucun /wallet/play n'est envoye,
	// et le betID n'est jamais presente comme un Event ID officiel.
	const onReplayRow = (round: HistoryRound) => {
		if (!canReplay) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		props.onclose();
		playBet(round.bet as never);
	};

	const onClose = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		props.onclose();
	};
</script>

<Container>
	<Rectangle
		anchor={0.5}
		width={PANEL_WIDTH}
		height={PANEL_HEIGHT}
		backgroundColor={0x1a0a14}
		borderColor={0xff2d6a}
		borderWidth={4}
	/>

	<Text
		y={-PANEL_HEIGHT / 2 + 34}
		anchor={0.5}
		text="HISTORY"
		style={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 28, fill: 0xff2d6a }}
	/>

	<!-- En-tetes -->
	<Text x={COL.time} y={TOP - 34} anchor={{ x: 0, y: 0.5 }} text="TIME" style={HEAD} />
	<Text x={COL.mode} y={TOP - 34} anchor={{ x: 0, y: 0.5 }} text="MODE" style={HEAD} />
	<Text x={COL.id} y={TOP - 34} anchor={{ x: 0, y: 0.5 }} text="ROUND ID" style={HEAD} />
	<Text x={COL.bet} y={TOP - 34} anchor={{ x: 1, y: 0.5 }} text="BET" style={HEAD} />
	<Text x={COL.win} y={TOP - 34} anchor={{ x: 1, y: 0.5 }} text="WIN" style={HEAD} />
	<Text x={COL.mult} y={TOP - 34} anchor={{ x: 1, y: 0.5 }} text="MULT" style={HEAD} />

	{#if rows.length === 0}
		<Text
			anchor={0.5}
			text="NO ROUNDS PLAYED YET"
			style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 22, fill: 0xff8fb3 }}
		/>
	{:else}
		{#each rows as round, i (round.key)}
			<Container
				y={TOP + i * ROW_GAP}
				eventMode={canReplay ? 'static' : 'none'}
				cursor={canReplay ? 'pointer' : 'default'}
				onpointerup={() => onReplayRow(round)}
			>
				<Rectangle
					anchor={0.5}
					width={PANEL_WIDTH - 60}
					height={ROW_HEIGHT}
					backgroundColor={i % 2 === 0 ? 0x260f1c : 0x1f0c17}
					borderColor={0x3a1526}
					borderWidth={1}
				/>
				<Text
					x={COL.time}
					anchor={{ x: 0, y: 0.5 }}
					text={round.date + '  ' + round.time}
					style={CELL}
				/>
				<Text x={COL.mode} anchor={{ x: 0, y: 0.5 }} text={round.mode} style={CELL} />
				<Text x={COL.id} anchor={{ x: 0, y: 0.5 }} text={round.id} style={CELL} />
				<Text
					x={COL.bet}
					anchor={{ x: 1, y: 0.5 }}
					text={numberToCurrencyString(round.betAmount)}
					style={CELL}
				/>
				<Text
					x={COL.win}
					anchor={{ x: 1, y: 0.5 }}
					text={numberToCurrencyString(round.winAmount)}
					style={{ ...CELL, fill: round.winAmount > 0 ? 0x4ade80 : 0xffffff }}
				/>
				<Text
					x={COL.mult}
					anchor={{ x: 1, y: 0.5 }}
					text={round.multiplier > 0 ? round.multiplier.toFixed(2) + 'x' : '-'}
					style={CELL}
				/>
			</Container>
		{/each}
	{/if}

	<!-- Pied de panneau -->
	<Text
		y={PANEL_HEIGHT / 2 - 76}
		anchor={0.5}
		text={canReplay
			? 'TAP A ROUND TO REPLAY IT LOCALLY - CURRENT SESSION ONLY'
			: 'CURRENT SESSION ONLY'}
		style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 15, fill: 0xff8fb3 }}
	/>

	<Container
		y={PANEL_HEIGHT / 2 - 38}
		eventMode="static"
		cursor="pointer"
		onpointerup={onClose}
	>
		<Rectangle
			anchor={0.5}
			width={240}
			height={46}
			backgroundColor={0x330018}
			borderColor={0xff2d6a}
			borderWidth={2}
		/>
		<Text
			anchor={0.5}
			text="CLOSE"
			style={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 22, fill: 0xffffff }}
		/>
	</Container>
</Container>
