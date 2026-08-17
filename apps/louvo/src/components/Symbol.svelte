<script lang="ts">
	import SymbolSpine from './SymbolSpine.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import { getSymbolInfo } from '../game/utils';
	import type { SymbolState, RawSymbol } from '../game/types';
	import { getContext } from '../game/context';
	import { BitmapText } from 'pixi-svelte';
	type Props = {
		x?: number;
		y?: number;
		state: SymbolState;
		rawSymbol: RawSymbol;
		oncomplete?: () => void;
		loop?: boolean;
	};
	const props: Props = $props();
	const context = getContext();
	const symbolInfo = $derived(getSymbolInfo({ rawSymbol: props.rawSymbol, state: props.state }));
	const isSprite = $derived(symbolInfo.type === 'sprite');
	// Louvo : M (MATCH) et K (SUPER LIKE) remplissent tout un rouleau quand ils
	// apparaissent - toujours affichés par-dessus le cadre de grille (zIndex 20
	// > zIndex 10 du cadre), pour un effet "rouleau étendu" bien visible.
	const isExpandingSymbol = $derived(props.rawSymbol.name === 'M' || props.rawSymbol.name === 'K');
	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 2; // pousse le sprite wild vers le bas de sa case (remonte de 3px supplementaires)
	const WILD_X_OFFSET = -3; // decale le sprite wild vers la gauche (~1mm)
	const MULTIPLIER_BADGE_Y_OFFSET = 27; // decale le badge sous le mot WILD (remonte de ~2mm)
	const adjustedX = $derived((props.x ?? 0) + (isWild ? WILD_X_OFFSET : 0));
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));
	const badgeY = $derived((props.y ?? 0) + (isWild ? MULTIPLIER_BADGE_Y_OFFSET : 0));
</script>
{#if isSprite}
	<SymbolSprite
		{symbolInfo}
		x={adjustedX}
		y={adjustedY}
		oncomplete={props.oncomplete}
		zIndex={isExpandingSymbol ? 20 : undefined}
	/>
{:else}
	<SymbolSpine
		loop={props.loop}
		{symbolInfo}
		x={props.x}
		y={props.y}
		showWinFrame={props.state === 'win' && !['S', 'M'].includes(props.rawSymbol.name)}
		listener={{
			complete: props.oncomplete,
			event: (_, event) => {
				if (event.data?.name === 'wildExplode') {
					context.eventEmitter?.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
				}
			},
		}}
	/>
{/if}
{#if props.rawSymbol.multiplier}
	<BitmapText
		anchor={0.5}
		x={props.x}
		y={badgeY}
		text={`${props.rawSymbol.multiplier}X`}
		zIndex={isExpandingSymbol ? 20 : undefined}
		style={{
			fontFamily: 'gold', fill: 0xffffff,
			fontSize: 34,
		}}
	/>
{/if}
