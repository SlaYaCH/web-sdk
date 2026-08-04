<script lang="ts">
	import { Sprite, type SpriteProps } from 'pixi-svelte';
	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_WIDTH, SYMBOL_HEIGHT } from '../game/constants';
	import { onMount } from 'svelte';
	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		oncomplete?: () => void;
		zIndex?: number;
	};
	const props: Props = $props();
	onMount(() => {
		props.oncomplete?.();
	});
	$effect(() => {
		props.symbolInfo;
		props.oncomplete?.();
	});
</script>
<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_WIDTH * props.symbolInfo.sizeRatios.width}
	height={SYMBOL_HEIGHT * props.symbolInfo.sizeRatios.height}
	zIndex={props.zIndex}
/>
