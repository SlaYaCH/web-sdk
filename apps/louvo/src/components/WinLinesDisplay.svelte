<script lang="ts" module>
	import type { Position } from '../game/types';
	export type EmitterEventWinLines = {
		type: 'winLinesShow';
		wins: { positions: Position[]; win: number }[];
	};
</script>

<script lang="ts">
	import { Container } from 'pixi-svelte';
	import { getContext } from '../game/context';
	import WinLineReveal from './WinLineReveal.svelte';
	import BoardContainer from './BoardContainer.svelte';

	const context = getContext();

	type ActiveWin = { id: number; positions: Position[]; amount: number };
	let activeWins = $state<ActiveWin[]>([]);
	let nextId = 0;

	const STAGGER_MS = 200;

	context.eventEmitter.subscribeOnMount({
		winLinesShow: async ({ wins }) => {
			for (const w of wins) {
				activeWins = [...activeWins, { id: nextId++, positions: w.positions, amount: w.win }];
				await new Promise((r) => setTimeout(r, STAGGER_MS));
			}
		},
	});

	const remove = (id: number) => {
		activeWins = activeWins.filter((w) => w.id !== id);
	};
</script>

<BoardContainer>
	{#snippet children()}
		{#each activeWins as win (win.id)}
			<WinLineReveal positions={win.positions} amount={win.amount} oncomplete={() => remove(win.id)} />
		{/each}
	{/snippet}
</BoardContainer>
