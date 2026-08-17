<script lang="ts">
	import { Container } from 'pixi-svelte';
	import AfterDarkHeartTally from './AfterDarkHeartTally.svelte';
	import DuelTierCard from './DuelTierCard.svelte';

	type Props = {
		filled: number;
		duelCardKey: string;
		duelAchieved?: boolean;
		matchCardKey?: string;
		matchAchieved?: boolean;
		presentoireSize: number;
		cardWidth: number;
		cardHeight: number;
		gap: number;
	};

	const props: Props = $props();

	const duelX = () => -(props.presentoireSize * 0.5 + props.gap + props.cardWidth * 0.5);
	const matchX = () => props.presentoireSize * 0.5 + props.gap + props.cardWidth * 0.5;
</script>

<Container>
	<AfterDarkHeartTally filled={props.filled} size={props.presentoireSize} />
	<Container x={duelX()}>
		<DuelTierCard
			cardKey={props.duelCardKey}
			width={props.cardWidth}
			height={props.cardHeight}
			achieved={props.duelAchieved}
		/>
	</Container>
	{#if props.matchCardKey}
		<Container x={matchX()}>
			<DuelTierCard
				cardKey={props.matchCardKey}
				width={props.cardWidth}
				height={props.cardHeight}
				achieved={props.matchAchieved}
			/>
		</Container>
	{/if}
</Container>
