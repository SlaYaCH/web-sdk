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
		// Coeurs deja lances par les autres Super Like du MEME tour (offset barillet).
		likesBefore: number;
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

	// Fermeture "au depart du rouleau" : une banniere fermee alors que SA
	// colonne est encore a l'arret decouvrirait la colonne de W du book
	// (vu en turbo/super turbo en bonus : les rouleaux partent en cascade,
	// un minuteur fixe fermait la banniere avant que son rouleau ne bouge).
	const scheduledCloseIds = new Set<number>();
	const closeWhenReelMoves = async (id: number, reelIndex: number) => {
		if (scheduledCloseIds.has(id)) return;
		scheduledCloseIds.add(id);
		const start = performance.now();
		while (
			context.stateGame.board[reelIndex]?.reelState.motion === 'stopped' &&
			performance.now() - start < 2000
		) {
			await new Promise((r) => setTimeout(r, 30));
		}
		activeReveals = activeReveals.map((r) =>
			r.id === id ? { ...r, closeToken: r.closeToken + 1 } : r,
		);
	};

	context.eventEmitter.subscribeOnMount({
		spinStart: () => {
			// Au DEPART de chaque rouleau, pas au clic : sinon la colonne de W
			// du book se decouvre avant que le rouleau ne bouge.
			activeReveals.forEach((r) => closeWhenReelMoves(r.id, r.reelIndex));
		},
		specialRevealShow: async (emitterEvent) => {
			const id = nextId++;
			// Une banniere d'un TOUR PRECEDENT encore sur le MEME rouleau : la
			// nouvelle se superpose (vu en Like Storm) et l'ancienne se ferme des
			// que son rouleau bouge - jamais avant (colonne de W dessous).
			activeReveals.forEach((r) => {
				if (r.reelIndex === emitterEvent.reelIndex && r.epoch < context.stateGame.bannerEpoch) {
					closeWhenReelMoves(r.id, r.reelIndex);
				}
			});
			await new Promise<void>((resolve) => {
				const reveal: ActiveReveal = {
					id,
					assetKey: emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal',
					multiplierText: `x${emitterEvent.multiplier}`,
					multiplier: emitterEvent.multiplier,
					duelValues: emitterEvent.duelValues,
					likePositions: emitterEvent.likePositions,
					likes: emitterEvent.likePositions?.length ?? 0,
					// Somme des coeurs des Super Like deja actifs sur CE tour : sert d'offset
					// pour que chaque barillet ne se vide qu'au rythme de SA distribution.
					likesBefore: activeReveals
						.filter((r) => r.assetKey === 'superlikeReveal' && r.epoch === context.stateGame.bannerEpoch)
						.reduce((sum, r) => sum + r.likes, 0),
					// Correction fine : bannieres des rouleaux 2-5 ~1mm trop a droite (valeur ajustable).
					bannerX: getSymbolX(emitterEvent.reelIndex) - (emitterEvent.reelIndex > 0 ? 2 : 0),
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
		// Saut de +2 = sortie de bonus (freeSpinEnd) : l'ecran est couvert par
		// la transition, fermeture immediate. Sinon (nouveau tour), chaque
		// banniere perimee ne se ferme que quand SON rouleau se met a bouger.
		const exitJump = epoch - lastEpoch >= 2;
		lastEpoch = epoch;
		if (exitJump) {
			activeReveals = activeReveals.map((r) =>
				r.epoch < epoch - 1 ? { ...r, closeToken: r.closeToken + 1 } : r,
			);
			return;
		}
		for (const r of activeReveals) {
			if (r.epoch < epoch - 1) closeWhenReelMoves(r.id, r.reelIndex);
		}
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
					likesBefore={reveal.likesBefore}
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
