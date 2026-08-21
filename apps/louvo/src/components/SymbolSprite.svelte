<script lang="ts">
	import { Sprite, type SpriteProps } from 'pixi-svelte';
	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_WIDTH, SYMBOL_HEIGHT } from '../game/constants';
	import { onMount } from 'svelte';
	import { stateGame } from '../game/stateGame.svelte';
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

	// 2% plus grand en After Dark (cadre plus grand que la base)
	const AFTER_DARK_SIZE_SCALE = 1.02;
	// Le symbole DATE (scatter S) est trop grand par rapport aux autres : -20 %.
	const DATE_SIZE_SCALE = 0.8;
	const sizeScale = $derived(
		(stateGame.tier === 'after_dark' ? AFTER_DARK_SIZE_SCALE : 1) *
			(props.symbolInfo.assetKey === 'S' ? DATE_SIZE_SCALE : 1),
	);
</script>

<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_WIDTH * props.symbolInfo.sizeRatios.width * sizeScale}
	height={SYMBOL_HEIGHT * props.symbolInfo.sizeRatios.height * sizeScale}
	zIndex={props.zIndex}
/>
