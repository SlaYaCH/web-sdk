<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Sprite, BitmapText } from 'pixi-svelte';
	import MatchDuelClash from './MatchDuelClash.svelte';
	import SuperlikeBarilletDisplay from './SuperlikeBarilletDisplay.svelte';
	import MatchOutcomeAnimation from './MatchOutcomeAnimation.svelte';
	import { SYMBOL_WIDTH, SYMBOL_HEIGHT, BOARD_DIMENSIONS } from '../game/constants';

	type Props = {
		assetKey: string;
		multiplierText?: string;
		duelValues?: [number, number];
		duelWinner?: number;
		likes?: number;
		forceClose?: boolean;
		x?: number;
		y?: number;
		durationInMs?: number;
		holdMs?: number;
		zIndex?: number;
		oncomplete?: () => void;
	};

	const props: Props = $props();
	const durationInMs = props.durationInMs ?? 350;
	const holdMs = props.holdMs ?? 1400;

	// Taille d'un rouleau complet : 1 colonne de large, toute la hauteur du plateau
	const bannerWidth = SYMBOL_WIDTH;
	const bannerHeight = SYMBOL_HEIGHT * BOARD_DIMENSIONS.y;

	let duelResolved = $state(false);
	const biggerWon = $derived(
		props.duelValues && props.duelWinner !== undefined
			? props.duelWinner === Math.max(props.duelValues[0], props.duelValues[1])
			: true,
	);

	let scale = $state(0.6);
	let alpha = $state(0);

	const easeOutBack = (t: number) => {
		const c1 = 1.70158;
		const c3 = c1 + 1;
		return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
	};

	const animateTo = (targetScale: number, targetAlpha: number, duration: number) =>
		new Promise<void>((resolve) => {
			const startScale = scale;
			const startAlpha = alpha;
			const start = performance.now();

			const step = (now: number) => {
				const elapsed = now - start;
				const t = Math.min(elapsed / duration, 1);
				const eased = easeOutBack(t);

				scale = startScale + (targetScale - startScale) * eased;
				alpha = startAlpha + (targetAlpha - startAlpha) * Math.min(elapsed / duration, 1);

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					scale = targetScale;
					alpha = targetAlpha;
					resolve();
				}
			};

			requestAnimationFrame(step);
		});

	let resolveHold = () => {};

	onMount(() => {
		(async () => {
			await animateTo(1, 1, durationInMs);

			if (holdMs > 0) {
				await Promise.race([
					new Promise<void>((r) => setTimeout(r, holdMs)),
					new Promise<void>((r) => (resolveHold = r)),
				]);
				await animateTo(1, 0, Math.min(durationInMs, 250));
			}

			props.oncomplete?.();
		})();
	});

	$effect(() => {
		if (props.forceClose) resolveHold();
	});
</script>

<Container x={props.x} y={props.y} alpha={alpha} scale={scale} zIndex={props.zIndex}>
	{#if props.assetKey === 'matchReveal' && duelResolved}
		<MatchOutcomeAnimation {biggerWon} width={bannerWidth} height={bannerHeight} />
	{:else}
		<Sprite anchor={0.5} key={props.assetKey} width={bannerWidth} height={bannerHeight} />
	{/if}

	{#if props.assetKey === 'matchReveal' && props.duelValues && props.duelWinner !== undefined}
		<MatchDuelClash
			duelValues={props.duelValues}
			winner={props.duelWinner}
			oncomplete={() => (duelResolved = true)}
		/>
	{:else if props.multiplierText}
		<BitmapText
			anchor={0.5}
			y={0}
			text={props.multiplierText}
			style={{
				fontFamily: 'gold', fill: 0xff2d6a,
				fontSize: 60,
			}}
		/>
	{/if}

	{#if props.assetKey === 'superlikeReveal' && props.likes}
		<SuperlikeBarilletDisplay likes={props.likes} />
	{/if}
</Container>
