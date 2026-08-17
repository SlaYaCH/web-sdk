<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>
<script lang="ts">
	import { Sprite } from 'pixi-svelte';
	import { getContext } from '../game/context';
	const context = getContext();
	const showBaseFrame = $derived(
		context.stateGame.gameType === 'basegame' || context.stateGame.tier === 'speed_dating',
	);
	const showFeatureFrame = $derived(context.stateGame.tier === 'after_dark');

	context.eventEmitter.subscribeOnMount({
		boardFrameGlowShow: () => {},
		boardFrameGlowHide: () => {},
	});
</script>
{#if showBaseFrame}
	<Sprite
		key="boardFrameOverlay"
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height * 0.5}
		anchor={0.5}
		width={context.stateLayoutDerived.mainLayout().width}
		height={context.stateLayoutDerived.mainLayout().height}
	/>
{/if}
{#if showFeatureFrame}
	<Sprite
		key="boardFrameOverlayAfterDark"
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height * 0.5}
		anchor={0.5}
		width={context.stateLayoutDerived.mainLayout().width}
		height={context.stateLayoutDerived.mainLayout().height}
	/>
{/if}
