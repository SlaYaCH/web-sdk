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
	import { dureesLignes, type PhasesLigne } from '../game/winLineSpeed.svelte';

	const context = getContext();

	type ActiveWin = {
		id: number;
		positions: Position[];
		amount: number;
		phases: PhasesLigne;
	};
	let activeWins = $state<ActiveWin[]>([]);
	let nextId = 0;

	context.eventEmitter.subscribeOnMount({
		winLinesShow: async ({ wins }) => {
			// UNE LIGNE A LA FOIS. Avant, chacune vivait 1520 ms et la
			// suivante partait 200 ms plus tard : avec cinq gains, cinq
			// lignes et cinq montants etaient a l'ecran en meme temps.
			// Maintenant l'ecart vaut la duree d'une ligne.
			//
			// dureesLignes est le SEUL calcul de cadence : le handler
			// winInfo lit le meme pour son attente finale, donc les deux
			// ne peuvent pas se contredire, turbo compris.
			const { phases, ecart } = dureesLignes(wins.length);
			for (const w of wins) {
				activeWins = [
					...activeWins,
					{ id: nextId++, positions: w.positions, amount: w.win, phases },
				];
				await new Promise((r) => setTimeout(r, ecart));
			}
		},
		spinStart: () => {
			// Filet de securite : un tour qui repart ne doit jamais laisser
			// derriere lui une ligne encore affichee.
			activeWins = [];
		},
	});

	const remove = (id: number) => {
		activeWins = activeWins.filter((w) => w.id !== id);
	};
</script>

<BoardContainer>
	{#snippet children()}
		{#each activeWins as win (win.id)}
			<WinLineReveal
				positions={win.positions}
				amount={win.amount}
				phases={win.phases}
				oncomplete={() => remove(win.id)}
			/>
		{/each}
	{/snippet}
</BoardContainer>
