<script lang="ts">
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { SECOND } from 'constants-shared/time';
	import { getContext } from '../game/context';
	const context = getContext();
	const showBaseBackground = $derived(
		context.stateGame.gameType === 'basegame' || context.stateGame.tier === 'speed_dating',
	);
	const showFeatureBackground = $derived(context.stateGame.tier === 'after_dark');
</script>
<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />
<MainContainer>
	<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-2}>
		<Sprite
			key="boardBackground"
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.5}
			anchor={0.5}
			width={context.stateLayoutDerived.mainLayout().width}
			height={context.stateLayoutDerived.mainLayout().height}
		/>
	</FadeContainer>
	<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-1}>
		<Sprite
			key="boardBackgroundAfterDark"
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.5}
			anchor={0.5}
			width={context.stateLayoutDerived.mainLayout().width}
			height={context.stateLayoutDerived.mainLayout().height}
		/>
	</FadeContainer>
</MainContainer>
