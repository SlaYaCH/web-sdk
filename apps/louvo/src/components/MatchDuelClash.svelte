<script lang="ts">
	import { onMount } from 'svelte';
	import { BitmapText } from 'pixi-svelte';

	type Props = {
		duelValues: [number, number];
		winner: number;
		oncomplete?: () => void;
	};
	const props: Props = $props();

	const SIDE_OFFSET = 28;
	const FONT_SIZE = 44;
	const WINNER_FONT_SIZE = 60;
	const Y_POSITION = 114; // pile entre le milieu (0) et le bas de la banniere
	const TEXT_Z_INDEX = 20; // toujours au-dessus de l'animation bisou/rupture qui suit

	let leftX = $state(-SIDE_OFFSET);
	let rightX = $state(SIDE_OFFSET);
	let leftScale = $state(0.4);
	let rightScale = $state(0.4);
	let leftAlpha = $state(0);
	let rightAlpha = $state(0);
	let showWinnerOnly = $state(false);

	const easeOutBack = (t: number) => {
		const c1 = 1.70158;
		const c3 = c1 + 1;
		return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
	};

	const popIn = () =>
		new Promise<void>((resolve) => {
			const duration = 300;
			const start = performance.now();
			const step = (now: number) => {
				const t = Math.min((now - start) / duration, 1);
				const eased = easeOutBack(t);
				leftScale = 0.4 + eased * 0.6;
				rightScale = 0.4 + eased * 0.6;
				leftAlpha = Math.min(t / 0.3, 1);
				rightAlpha = Math.min(t / 0.3, 1);
				if (t < 1) requestAnimationFrame(step);
				else resolve();
			};
			requestAnimationFrame(step);
		});

	const resolveDuel = () =>
		new Promise<void>((resolve) => {
			const isLeftWinner = props.duelValues[0] === props.winner;
			const duration = 450;
			const start = performance.now();
			const startLeftX = leftX;
			const startRightX = rightX;

			const step = (now: number) => {
				const t = Math.min((now - start) / duration, 1);
				const eased = easeOutBack(t);

				if (isLeftWinner) {
					leftX = startLeftX + (0 - startLeftX) * eased;
					leftScale = 1 + eased * 0.35;
					rightScale = Math.max(1 - t * 1.2, 0);
					rightAlpha = Math.max(1 - t * 1.5, 0);
				} else {
					rightX = startRightX + (0 - startRightX) * eased;
					rightScale = 1 + eased * 0.35;
					leftScale = Math.max(1 - t * 1.2, 0);
					leftAlpha = Math.max(1 - t * 1.5, 0);
				}

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					showWinnerOnly = true;
					resolve();
				}
			};
			requestAnimationFrame(step);
		});

	onMount(() => {
		(async () => {
			await popIn();
			await new Promise((r) => setTimeout(r, 450));
			await resolveDuel();
			props.oncomplete?.();
		})();
	});
</script>

{#if !showWinnerOnly}
	<BitmapText
		anchor={0.5}
		x={leftX}
		y={Y_POSITION}
		scale={leftScale}
		alpha={leftAlpha}
		zIndex={TEXT_Z_INDEX}
		text={`x${props.duelValues[0]}`}
		style={{ fontFamily: 'gold', fontSize: FONT_SIZE, fill: 0xff2d6a }}
	/>
	<BitmapText
		anchor={0.5}
		x={rightX}
		y={Y_POSITION}
		scale={rightScale}
		alpha={rightAlpha}
		zIndex={TEXT_Z_INDEX}
		text={`x${props.duelValues[1]}`}
		style={{ fontFamily: 'gold', fontSize: FONT_SIZE, fill: 0xff2d6a }}
	/>
{:else}
	<BitmapText
		anchor={0.5}
		y={Y_POSITION}
		zIndex={TEXT_Z_INDEX}
		text={`x${props.winner}`}
		style={{ fontFamily: 'gold', fontSize: WINNER_FONT_SIZE, fill: 0xff2d6a }}
	/>
{/if}
