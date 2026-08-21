<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { anchorToPivot, BitmapText, Container, Rectangle, type Sizes } from 'pixi-svelte';

	const context = getContext();

	const panelSizes = $derived({
		width: SYMBOL_SIZE * 1.53,
		height: SYMBOL_SIZE * 0.61,
	});
	// Miroir exact du compteur de free spins, a droite du centre de la grille.
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x - panelSizes.width * 0.5 + SYMBOL_SIZE * 1.0,
		y:
			context.stateGameDerived.boardLayout().y +
			context.stateGameDerived.boardLayout().height * 0.5 +
			SYMBOL_SIZE * 0.2,
	});

	const fontSize = SYMBOL_SIZE * 0.21;
	// Visible UNIQUEMENT pendant les free spins (Speed Dating / After Dark) -
	// jamais en base game ni avec un simple mode active.
	const show = $derived(context.stateGame.gameType === 'freegame');

	let titleSizes: Sizes = $state({ width: 0, height: 0 });
	let amountSizes: Sizes = $state({ width: 0, height: 0 });
	const textContainerSizes = $derived({
		width: Math.max(titleSizes.width, amountSizes.width),
		height: titleSizes.height + amountSizes.height,
	});
</script>

<MainContainer>
	<FadeContainer {show} {...position} scale={1}>
		<Rectangle {...panelSizes} backgroundColor={0x000000} backgroundAlpha={0.78} />
		<Container
			x={panelSizes.width * 0.5}
			y={panelSizes.height * 0.48}
			pivot={anchorToPivot({
				sizes: textContainerSizes,
				anchor: { x: 0.5, y: 0.5 },
			})}
		>
			<BitmapText
				anchor={{ x: 0.5, y: 0 }}
				x={textContainerSizes.width * 0.5}
				text={'TOTAL WIN'}
				style={{
					fontFamily: 'gold', fill: 0xff2d6a,
					fontSize,
					wordWrap: false,
				}}
				onresize={(sizes) => (titleSizes = sizes)}
			/>
			<BitmapText
				anchor={{ x: 0.5, y: 0 }}
				x={textContainerSizes.width * 0.5}
				y={titleSizes.height}
				text={bookEventAmountToCurrencyString(stateBet.winBookEventAmount)}
				style={{
					fontFamily: 'gold', fill: 0xffffff,
					fontSize,
				}}
				onresize={(sizes) => (amountSizes = sizes)}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
