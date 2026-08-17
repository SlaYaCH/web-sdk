<script lang="ts">
	import { Container } from 'pixi-svelte';
	import { getContext } from '../game/context';
	import { GRID_LEFT_FRAC, GRID_RIGHT_FRAC, GRID_TOP_FRAC, GRID_BOTTOM_FRAC } from '../game/constants';
	import AfterDarkStreakGroup from './AfterDarkStreakGroup.svelte';

	type GroupState = { filled: number; achieved: boolean };

	type Props = {
		tier2?: GroupState;
		tier3?: GroupState;
		tier4?: GroupState;
		tier5x?: GroupState;
	};

	const props: Props = $props();
	const context = getContext();

	// ============================================================
	// REGLAGES RAPIDES
	// ============================================================
	const PRESENTOIRE_SIZE = 130;
	const CARD_WIDTH = 90;
	const CARD_HEIGHT = 120;
	const GAP = 14;
	const GROUP_Y_FRACS = [0.27, 0.73];
	// ============================================================

	const mainW = () => context.stateLayoutDerived.mainLayout().width;
	const mainH = () => context.stateLayoutDerived.mainLayout().height;

	const leftX = () => mainW() * (GRID_LEFT_FRAC * 0.5);
	const rightX = () => mainW() * (GRID_RIGHT_FRAC + (1 - GRID_RIGHT_FRAC) * 0.5);
	const groupY = (i: number) =>
		mainH() * (GRID_TOP_FRAC + (GRID_BOTTOM_FRAC - GRID_TOP_FRAC) * GROUP_Y_FRACS[i]);

	const t2 = () => props.tier2 ?? { filled: 0, achieved: false };
	const t3 = () => props.tier3 ?? { filled: 0, achieved: false };
	const t4 = () => props.tier4 ?? { filled: 0, achieved: false };
	const t5x = () => props.tier5x ?? { filled: 0, achieved: false };
</script>

{#if context.stateGame.tier === 'after_dark'}
	<Container x={leftX()} y={groupY(0)}>
		<AfterDarkStreakGroup
			filled={t2().filled}
			duelCardKey="duelPlus2"
			duelAchieved={t2().achieved}
			matchCardKey="matchPlus3"
			matchAchieved={t2().achieved}
			presentoireSize={PRESENTOIRE_SIZE}
			cardWidth={CARD_WIDTH}
			cardHeight={CARD_HEIGHT}
			gap={GAP}
		/>
	</Container>
	<Container x={leftX()} y={groupY(1)}>
		<AfterDarkStreakGroup
			filled={t3().filled}
			duelCardKey="duelPlus3"
			duelAchieved={t3().achieved}
			matchCardKey="matchPlus3"
			matchAchieved={t3().achieved}
			presentoireSize={PRESENTOIRE_SIZE}
			cardWidth={CARD_WIDTH}
			cardHeight={CARD_HEIGHT}
			gap={GAP}
		/>
	</Container>
	<Container x={rightX()} y={groupY(0)}>
		<AfterDarkStreakGroup
			filled={t4().filled}
			duelCardKey="duelPlus4"
			duelAchieved={t4().achieved}
			matchCardKey="matchPlus3"
			matchAchieved={t4().achieved}
			presentoireSize={PRESENTOIRE_SIZE}
			cardWidth={CARD_WIDTH}
			cardHeight={CARD_HEIGHT}
			gap={GAP}
		/>
	</Container>
	<Container x={rightX()} y={groupY(1)}>
		<AfterDarkStreakGroup
			filled={t5x().filled}
			duelCardKey="duel5x"
			duelAchieved={t5x().achieved}
			presentoireSize={PRESENTOIRE_SIZE}
			cardWidth={CARD_WIDTH}
			cardHeight={CARD_HEIGHT}
			gap={GAP}
		/>
	</Container>
{/if}
