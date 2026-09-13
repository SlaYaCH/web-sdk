<script lang="ts">
	import SymbolSpine from './SymbolSpine.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import SymbolPack from './SymbolPack.svelte';
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
	const isPack = $derived(symbolInfo.type === 'pack');
	const packName = $derived((symbolInfo as { pack?: string }).pack ?? '');
	// Louvo : M (MATCH) et K (SUPER LIKE) remplissent tout un rouleau quand ils
	// apparaissent - toujours affichés par-dessus le cadre de grille (zIndex 20
	// > zIndex 10 du cadre), pour un effet "rouleau étendu" bien visible.
	const isExpandingSymbol = $derived(props.rawSymbol.name === 'M' || props.rawSymbol.name === 'K');
	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 0; // pack V6 : le nouveau WILD remplit sa case, plus de rattrapage
	const WILD_X_OFFSET = 0; // pack V6 : idem
	const MULTIPLIER_BADGE_Y_OFFSET = 27; // decale le badge sous le mot WILD (remonte de ~2mm)
	const adjustedX = $derived((props.x ?? 0) + (isWild ? WILD_X_OFFSET : 0));
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));
	const badgeY = $derived((props.y ?? 0) + (isWild ? MULTIPLIER_BADGE_Y_OFFSET : 0));
</script>
{#if isPack}
	<!-- Pack V6. La cle sur packName fait repartir l'animation
	     quand le symbole change, et seulement alors : land et win
	     partagent le meme nom, donc l'atterrissage enchaine sur la
	     boucle de gain sans coupure. -->
	{#key packName}
		<SymbolPack
			{symbolInfo}
			x={adjustedX}
			y={adjustedY}
			loop={props.state === 'win'}
			oncomplete={props.oncomplete}
			zIndex={isExpandingSymbol ? 20 : undefined}
		/>
	{/key}
{:else if isSprite}
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
{#if (props.rawSymbol.multiplier) > 1}
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
