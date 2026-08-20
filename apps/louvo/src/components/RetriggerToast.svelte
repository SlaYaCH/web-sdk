<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle, BitmapText } from 'pixi-svelte';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	let visibleAmount = $state(0);
	let hideTimer: ReturnType<typeof setTimeout> | null = null;

	$effect(() => {
		const amount = context.stateGame.retriggerToShow;
		if (amount > 0) {
			visibleAmount = amount;
			if (hideTimer) clearTimeout(hideTimer);
			hideTimer = setTimeout(() => {
				visibleAmount = 0;
				context.stateGame.retriggerToShow = 0;
			}, 1600);
		}
	});
</script>

{#if visibleAmount > 0}
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y - SYMBOL_SIZE * 1.4}
		>
			<Rectangle
				anchor={0.5}
				width={SYMBOL_SIZE * 3}
				height={SYMBOL_SIZE * 0.7}
				backgroundColor={0x000000}
				alpha={0.78}
			/>
			<BitmapText
				anchor={0.5}
				text={`+${visibleAmount} FREE SPINS`}
				style={{
					fontFamily: 'gold', fill: 0xff2d6a,
					fontSize: SYMBOL_SIZE * 0.32,
					fontWeight: 'bold',
				}}
			/>
		</Container>
	</MainContainer>
{/if}
