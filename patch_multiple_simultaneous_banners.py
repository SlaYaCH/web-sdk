results = []

# --- 1) SpecialRevealOverlay.svelte : reecriture complete en tableau ---
path1 = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
new1 = """<script lang=\"ts\" module>
	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
		duelValues?: [number, number];
		likePositions?: { reelIndex: number; rowIndex: number }[];
	};
</script>
<script lang=\"ts\">
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
					resolve,
				};
				activeReveals = [...activeReveals, reveal];
				syncActiveBannerReelIndexes();
			});
			activeReveals = activeReveals.filter((r) => r.id !== id);
			syncActiveBannerReelIndexes();
		},
	});
</script>
{#if activeReveals.length > 0}
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
{/if}
"""
with open(path1, "w") as f:
    f.write(new1)
results.append("OK (SpecialRevealOverlay.svelte reecrit, supporte plusieurs bannieres simultanees)")

# --- 2) stateGame.svelte.ts : champ singulier -> tableau ---
path2 = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path2, "r") as f:
    c2 = f.read()
old2 = "activeBannerReelIndex: null as number | null,"
new2 = "activeBannerReelIndexes: [] as number[],"
n = c2.count(old2)
if n != 1:
    results.append(f"ERREUR (stateGame) : {n} fois.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK (stateGame : champ passe en tableau)")

# --- 3) Anticipations.svelte : verifier contre le tableau ---
path3 = "apps/louvo/src/components/Anticipations.svelte"
with open(path3, "r") as f:
    c3 = f.read()
old3a = "reel.reelState.anticipating && reel.reelIndex !== context.stateGame.activeBannerReelIndex,"
new3a = "reel.reelState.anticipating && !context.stateGame.activeBannerReelIndexes.includes(reel.reelIndex),"
n = c3.count(old3a)
if n != 1:
    results.append(f"ERREUR (Anticipations hasAnticipation) : {n} fois.")
else:
    c3 = c3.replace(old3a, new3a, 1)
    results.append("OK (Anticipations hasAnticipation)")

old3b = "{#if reel.reelState.anticipating && reel.reelIndex !== context.stateGame.activeBannerReelIndex}"
new3b = "{#if reel.reelState.anticipating && !context.stateGame.activeBannerReelIndexes.includes(reel.reelIndex)}"
n = c3.count(old3b)
if n != 1:
    results.append(f"ERREUR (Anticipations each) : {n} fois.")
else:
    c3 = c3.replace(old3b, new3b, 1)
    results.append("OK (Anticipations each)")
with open(path3, "w") as f:
    f.write(c3)

# --- 4) SuperlikeHeartThrow.svelte : verifier contre le tableau ---
path4 = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path4, "r") as f:
    c4 = f.read()
old4 = "(p) => p.reelIndex !== props.reelIndex && p.reelIndex !== context.stateGame.activeBannerReelIndex,"
new4 = "(p) => p.reelIndex !== props.reelIndex && !context.stateGame.activeBannerReelIndexes.includes(p.reelIndex),"
n = c4.count(old4)
if n != 1:
    results.append(f"ERREUR (SuperlikeHeartThrow) : {n} fois.")
else:
    c4 = c4.replace(old4, new4, 1)
    with open(path4, "w") as f:
        f.write(c4)
    results.append("OK (SuperlikeHeartThrow)")

for r in results:
    print(r)
