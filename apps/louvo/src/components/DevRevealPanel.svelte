<script lang="ts">
	import { getContext } from '../game/context';
	import { stateBet } from 'state-shared';

	const context = getContext();

	const REEL_COUNT = 5;
	let symbol = $state<'M' | 'K'>('M');
	let multiplier = $state(7);
	let secondDuelValue = $state(3);
	let likesCount = $state(3);
	let streakTierTest = $state(0);

	const trigger = (reelIndex: number) => {
		// Reproduit fidelement la vraie logique _fire_likes du Math SDK :
		// jamais de doublon, jamais sur la colonne deja wild de la banniere.
		let likePositions: { reelIndex: number; rowIndex: number }[] | undefined;
		if (symbol === 'K') {
			const candidates: { reelIndex: number; rowIndex: number }[] = [];
			for (let r = 0; r < REEL_COUNT; r++) {
				if (r === reelIndex) continue;
				for (let row = 0; row < REEL_COUNT; row++) {
					candidates.push({ reelIndex: r, rowIndex: row });
				}
			}
			for (let i = candidates.length - 1; i > 0; i--) {
				const j = Math.floor(Math.random() * (i + 1));
				[candidates[i], candidates[j]] = [candidates[j], candidates[i]];
			}
			likePositions = candidates.slice(0, likesCount);
		}

		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
			likePositions,
		});
		if (symbol === 'K') {
			context.stateGame.streakTier = streakTierTest;
			context.stateGame.streakLikes = likesCount;
		}
	};

	const setTier = (tier: 'basegame' | 'speed_dating' | 'after_dark') => {
		context.stateGame.gameType = tier === 'basegame' ? 'basegame' : 'freegame';
		context.stateGame.tier = tier;
		const musicName =
			tier === 'after_dark' ? 'bgm_after_dark' : tier === 'speed_dating' ? 'bgm_speed_dating' : 'bgm_main_louvo';
		context.eventEmitter.broadcast({ type: 'soundMusic', name: musicName });
	};
</script>

{#if import.meta.env.DEV}
	<div class="dev-panel">
		<div class="dev-panel__row">
			<button class:active={symbol === 'M'} onclick={() => (symbol = 'M')}>MATCH</button>
			<button class:active={symbol === 'K'} onclick={() => (symbol = 'K')}>SUPER LIKE</button>
			<label>
				x
				<input type="number" min="1" max="50" bind:value={multiplier} />
			</label>
			{#if symbol === 'M'}
				<label>
					vs x
					<input type="number" min="1" max="50" bind:value={secondDuelValue} />
				</label>
			{/if}
			{#if symbol === 'K'}
				<label>
					likes
					<input type="number" min="1" max="6" bind:value={likesCount} />
				</label>
				<label>
					streak (0-4)
					<input type="number" min="0" max="4" bind:value={streakTierTest} />
				</label>
			{/if}
		</div>
		<div class="dev-panel__row">
			{#each Array.from({ length: REEL_COUNT }) as _, reelIndex}
				<button onclick={() => trigger(reelIndex)}>Rouleau {reelIndex + 1}</button>
			{/each}
		</div>
		<div class="dev-panel__row">
			<button
				onclick={() => {
					stateBet.balanceAmount = 1000;
				}}
			>
				Crediter 1000
			</button>
		</div>
		<div class="dev-panel__row">
			<button onclick={() => setTier('basegame')}>Base</button>
			<button onclick={() => setTier('speed_dating')}>Speed Dating</button>
			<button onclick={() => setTier('after_dark')}>After Dark</button>
		</div>
		<div class="dev-panel__row">
			<button
				onclick={() => {
					context.stateGame.streakTier = 0;
					context.stateGame.streakLikes = 0;
				}}
			>
				Reset streak
			</button>
		</div>
	</div>
{/if}

<style>
	.dev-panel {
		position: fixed;
		top: 8px;
		bottom: 8px;
		left: 8px;
		width: 140px;
		z-index: 9999;
		background: rgba(0, 0, 0, 0.75);
		border: 1px solid #ff4d8d;
		border-radius: 8px;
		padding: 8px;
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-family: sans-serif;
		font-size: 12px;
		overflow-y: auto;
	}
	.dev-panel__row {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		align-items: center;
	}
	.dev-panel button {
		background: #222;
		color: #fff;
		border: 1px solid #555;
		border-radius: 4px;
		padding: 4px 8px;
		cursor: pointer;
	}
	.dev-panel button.active {
		background: #ff4d8d;
		border-color: #ff4d8d;
	}
	.dev-panel input {
		width: 48px;
	}
</style>
