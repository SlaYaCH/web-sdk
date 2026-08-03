<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>
<script lang="ts">
	import { Sprite } from 'pixi-svelte';
	import { getContext } from '../game/context';
	const context = getContext();
	const frameProps = $derived(context.stateLayoutDerived.normalBackgroundLayout({}));
	const showBaseFrame = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureFrame = $derived(context.stateGame.gameType === 'freegame');

	context.eventEmitter.subscribeOnMount({
		boardFrameGlowShow: () => {},
		boardFrameGlowHide: () => {},
	});
</script>
{#if showBaseFrame}
	<Sprite key="boardFrameOverlay" zIndex={10} {...frameProps} />
{/if}
{#if showFeatureFrame}
	<Sprite key="boardFrameOverlayAfterDark" zIndex={10} {...frameProps} />
{/if}
