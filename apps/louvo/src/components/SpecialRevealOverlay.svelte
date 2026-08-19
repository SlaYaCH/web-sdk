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
	import { getContext } from '../game/context';
	import { getSymbolX } from '../game/utils';
	import { BOARD_SIZES } from '../game/constants';
	import BoardContainer from './BoardContainer.svelte';
	import BannerReveal from './BannerReveal.svelte';
	import SuperlikeHeartThrow from './SuperlikeHeartThrow.svelte';
	const context = getContext();

	// Plusieurs bannieres (Match Duel/Super Like) peuvent etre actives EN MEME
	// TEMPS sur le meme spin (ex: 2 MATCH garantis par match_frenzy) - un
	// tableau au lieu de variables uniques evite qu'une nouvelle banniere
	// n'ecrase/remplace une precedente encore affichee.
	type ActiveReveal = {
		id: number;
		assetKey: 'matchReveal' | 'superlikeReveal';
		multiplierText: string;
		multiplier: number;
		duelValues?: [number, number];
		likePositions?: { reelIndex: number; rowIndex: number }[];
		likes: number;
		bannerX: number;
		reelIndex: number;
		closeToken: number;
		epoch: number;
		resolve: () => void;
	};

	let activeReveals = $state<ActiveReveal[]>([]);
	let nextId = 0;

	const syncActiveBannerReelIndexes = () => {
		context.stateGame.activeBannerReelIndexes = activeReveals.map((r) => r.reelIndex);
	};

	context.eventEmitter.subscribeOnMount({
		spinStart: () => {
			activeReveals = activeReveals.map((r) => ({ ...r, closeToken: r.closeToken + 1 }));
		},
		specialRevealShow: async (emitterEvent) => {
			const id = nextId++;
			await new Promise<void>((resolve) => {
				const reveal: ActiveReveal = {
					id,
					assetKey: emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal',
					multiplierText: `x${emitterEvent.multiplier}`,
					multiplier: emitterEvent.multiplier,
					duelValues: emitterEvent.duelValues,
					likePositions: emitterEvent.likePositions,
					likes: emitterEvent.likePositions?.length ?? 0,
					bannerX: getSymbolX(emitterEvent.reelIndex),
					reelIndex: emitterEvent.reelIndex,
					closeToken: 0,
					epoch: context.stateGame.bannerEpoch,
					resolve,
				};
				activeReveals = [...activeReveals, reveal];
				syncActiveBannerReelIndexes();
			});
			activeReveals = activeReveals.filter((r) => r.id !== id);
			syncActiveBannerReelIndexes();
		},
	});

	// bannerEpoch est incremente par le handler reveal a chaque nouveau tour
	// (free spins compris) : on ferme les bannieres des tours precedents,
	// celles du tour courant sont epargnees.
	let lastEpoch = 0;
	$effect(() => {
		const epoch = context.stateGame.bannerEpoch;
		if (epoch === lastEpoch) return;
		lastEpoch = epoch;
		activeReveals = activeReveals.map((r) =>
			r.epoch < epoch - 1 ? { ...r, closeToken: r.closeToken + 1 } : r
		);
	});
</script>
	<MainContainer>
		<BoardContainer>
			{#each activeReveals as reveal (reveal.id)}
				<BannerReveal
					assetKey={reveal.assetKey}
					multiplierText={reveal.multiplierText}
					duelValues={reveal.duelValues}
					duelWinner={reveal.multiplier}
					likes={reveal.likes}
					x={reveal.bannerX}
					y={BOARD_SIZES.height / 2}
					zIndex={30}
					holdMs={Infinity}
					closeToken={reveal.closeToken}
					oncomplete={() => reveal.resolve()}
				/>
				{#if reveal.assetKey === 'superlikeReveal'}
					<SuperlikeHeartThrow reelIndex={reveal.reelIndex} positions={reveal.likePositions} />
				{/if}
			{/each}
		</BoardContainer>
	</MainContainer>
