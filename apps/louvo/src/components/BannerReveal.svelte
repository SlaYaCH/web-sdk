<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Sprite, BitmapText } from 'pixi-svelte';
	import { SYMBOL_WIDTH, SYMBOL_HEIGHT, BOARD_DIMENSIONS } from '../game/constants';

	type Props = {
		assetKey: string;
		multiplierText?: string;
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

	onMount(() => {
		(async () => {
			await animateTo(1, 1, durationInMs);

			if (holdMs > 0) {
				await new Promise((r) => setTimeout(r, holdMs));
				await animateTo(1, 0, Math.min(durationInMs, 250));
			}

			props.oncomplete?.();
		})();
	});
</script>

<Container x={props.x} y={props.y} alpha={alpha} scale={scale} zIndex={props.zIndex}>
	<Sprite anchor={0.5} key={props.assetKey} width={bannerWidth} height={bannerHeight} />

	{#if props.multiplierText}
		<BitmapText
			anchor={0.5}
			y={0}
			text={props.multiplierText}
			style={{
				fontFamily: 'gold',
				fontSize: 60,
			}}
		/>
	{/if}
</Container>
