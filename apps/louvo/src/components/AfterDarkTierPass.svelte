<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	// Palier 1 garantit 2 MATCH, palier 2 -> 3, palier 3 -> 4, palier 4 -> 5x.
	const DUEL_CARD_BY_TIER: Record<number, string> = {
		1: 'duelPlus2',
		2: 'duelPlus3',
		3: 'duelPlus4',
		4: 'duel5x',
	};

	let visibleTier = $state(0);
	let hideTimer: ReturnType<typeof setTimeout> | null = null;

	$effect(() => {
		const tier = context.stateGame.tierPassToShow;
		if (tier > 0) {
			visibleTier = tier;
			if (hideTimer) clearTimeout(hideTimer);
			hideTimer = setTimeout(() => {
				visibleTier = 0;
				context.stateGame.tierPassToShow = 0;
			}, 1800);
		}
	});

	const cardWidth = SYMBOL_SIZE * 3.2;
	const cardHeight = SYMBOL_SIZE * 4.4;

	// La carte "+3 tours" n'accompagne que les trois premiers paliers.
	// Le 4e n'accorde pas de tours supplementaires : il ne montre que
	// sa propre carte. Elle etait dessinee sans condition - d'ou les
	// deux cartes au 4e palier.
	const MATCH_CARD_BY_TIER: Record<number, string> = {
		1: 'matchPlus3',
		2: 'matchPlus3',
		3: 'matchPlus3',
	};

	const carteMatch = $derived(MATCH_CARD_BY_TIER[visibleTier]);
	// Seule, la carte du palier se centre au lieu de rester decalee a
	// gauche comme si sa voisine etait toujours la.
	const carteDuelX = $derived(carteMatch ? -cardWidth * 0.55 : 0);
</script>

{#if visibleTier > 0 && DUEL_CARD_BY_TIER[visibleTier]}
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
		>
			<Sprite
				anchor={0.5}
				x={carteDuelX}
				key={DUEL_CARD_BY_TIER[visibleTier]}
				width={cardWidth}
				height={cardHeight}
			/>
			{#if carteMatch}
				<Sprite
					anchor={0.5}
					x={cardWidth * 0.55}
					key={carteMatch}
					width={cardWidth}
					height={cardHeight}
				/>
			{/if}
		</Container>
	</MainContainer>
{/if}
