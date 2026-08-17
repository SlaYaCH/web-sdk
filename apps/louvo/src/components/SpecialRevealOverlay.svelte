<script lang="ts" module>
	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
		duelValues?: [number, number];
		likePositions?: { reelIndex: number; rowIndex: number }[];
	};
</script>

<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { waitForResolve } from 'utils-shared/wait';
	import { getContext } from '../game/context';
	import { getSymbolX } from '../game/utils';
	import { BOARD_SIZES } from '../game/constants';
	import BoardContainer from './BoardContainer.svelte';
	import BannerReveal from './BannerReveal.svelte';
import SuperlikeHeartThrow from './SuperlikeHeartThrow.svelte';

	const context = getContext();

	let show = $state(false);
	let assetKey = $state<'matchReveal' | 'superlikeReveal'>('matchReveal');
	let multiplierText = $state('');
	let multiplier = $state(0);
	let duelValues = $state<[number, number] | undefined>(undefined);
	let likePositions = $state<{ reelIndex: number; rowIndex: number }[] | undefined>(undefined);
	let likes = $state(0);
	let bannerX = $state(0);
	let forceClose = $state(false);
	let revealReelIndex = $state(0);
	let resolveShow = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		spinStart: () => {
			if (show) forceClose = true;
		},
		specialRevealShow: async (emitterEvent) => {
			forceClose = false;
			assetKey = emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal';
			multiplierText = `x${emitterEvent.multiplier}`;
			multiplier = emitterEvent.multiplier;
			duelValues = emitterEvent.duelValues;
			likePositions = emitterEvent.likePositions;
			likes = emitterEvent.likePositions?.length ?? 0;
			bannerX = getSymbolX(emitterEvent.reelIndex);
			revealReelIndex = emitterEvent.reelIndex;
			show = true;
			await waitForResolve((resolve) => (resolveShow = resolve));
			show = false;
		},
	});
</script>

{#if show}
	<MainContainer>
		<BoardContainer>
			<BannerReveal
				{assetKey}
				{multiplierText}
				duelValues={duelValues}
				duelWinner={multiplier}
				likes={likes}
				x={bannerX}
				y={BOARD_SIZES.height / 2}
				zIndex={30}
				holdMs={6000}
				forceClose={forceClose}
				oncomplete={() => resolveShow()}
			/>

			{#if assetKey === 'superlikeReveal'}
				<SuperlikeHeartThrow reelIndex={revealReelIndex} positions={likePositions} />
			{/if}
		</BoardContainer>
	</MainContainer>
{/if}
