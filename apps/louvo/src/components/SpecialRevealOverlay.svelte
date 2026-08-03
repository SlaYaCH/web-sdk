<script lang="ts" module>
	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
	};
</script>

<script lang="ts">
	import { waitForResolve } from 'utils-shared/wait';
	import { getContext } from '../game/context';
	import { getSymbolX } from '../game/utils';
	import { BOARD_SIZES } from '../game/constants';
	import BannerReveal from './BannerReveal.svelte';

	const context = getContext();

	let show = $state(false);
	let assetKey = $state<'matchReveal' | 'superlikeReveal'>('matchReveal');
	let multiplierText = $state('');
	let bannerX = $state(0);
	let resolveShow = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		specialRevealShow: async (emitterEvent) => {
			assetKey = emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal';
			multiplierText = `x${emitterEvent.multiplier}`;
			bannerX = getSymbolX(emitterEvent.reelIndex);
			show = true;
			await waitForResolve((resolve) => (resolveShow = resolve));
			show = false;
		},
	});
</script>

{#if show}
	<BannerReveal
		{assetKey}
		{multiplierText}
		x={bannerX}
		y={BOARD_SIZES.height / 2}
		zIndex={30}
		oncomplete={() => resolveShow()}
	/>
{/if}
