<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';
	import { getSymbolX } from '../game/utils';
	import { getContext } from '../game/context';
	import { BOARD_SIZES, SYMBOL_HEIGHT, REEL_PADDING } from '../game/constants';

	type Position = { reelIndex: number; rowIndex: number };

	type Props = {
		reelIndex: number;
		positions?: Position[];
	};
	const props: Props = $props();
	const context = getContext();

	const HEART_SIZE = 28; // meme taille que les coeurs du presentoir
	const BASE_DELAY = 300;

	const originX = getSymbolX(props.reelIndex);
	const originY = BOARD_SIZES.height / 2 + 162.7;

	const getRowY = (rowIndex: number) => SYMBOL_HEIGHT * (rowIndex + REEL_PADDING);

	const targets = (props.positions ?? []).map((p) => ({
		x: getSymbolX(p.reelIndex),
		y: getRowY(p.rowIndex),
	}));

	type Heart = { id: number; x: number; y: number; alpha: number; scale: number };

	let hearts = $state<Heart[]>(
		targets.map((_, i) => ({ id: i, x: originX, y: originY, alpha: 0, scale: 0.5 })),
	);

	const easeOutQuad = (t: number) => 1 - (1 - t) * (1 - t);

	const fadeOut = (index: number) =>
		new Promise<void>((resolve) => {
			const duration = 180;
			const start = performance.now();

			const step = (now: number) => {
				const t = Math.min((now - start) / duration, 1);
				hearts[index].alpha = 1 - t;

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					resolve();
				}
			};

			requestAnimationFrame(step);
		});

	// Vole vers la cible et resout des que le coeur touche sa case - le
	// fondu de disparition part APRES en arriere-plan (fire-and-forget),
	// sans retarder le lancer du coeur suivant.
	const flyTo = (index: number) =>
		new Promise<void>((resolve) => {
			const target = targets[index];
			const duration = 550;
			const arcHeight = 60 + Math.random() * 30;
			const start = performance.now();

			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up', forcePlay: true });

			const step = (now: number) => {
				const elapsed = now - start;
				const t = Math.min(elapsed / duration, 1);
				const eased = easeOutQuad(t);

				hearts[index].x = originX + (target.x - originX) * eased;
				hearts[index].y =
					originY + (target.y - originY) * eased - Math.sin(t * Math.PI) * arcHeight;
				hearts[index].alpha = t < 0.15 ? t / 0.15 : 1;
				hearts[index].scale = 0.5 + Math.min(t / 0.2, 1) * 0.5;

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					// Le symbole devient WILD exactement au moment ou le coeur
					// touche sa case (pas avant, pas apres).
					const pos = props.positions?.[index];
					if (pos) {
						const reelSymbol =
							context.stateGame.board[pos.reelIndex]?.reelState?.symbols[pos.rowIndex + 1];
						if (reelSymbol) {
							reelSymbol.rawSymbol = { name: 'W', wild: true };
						}
					}
					context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode', forcePlay: true });
					// Le coeur disparait immediatement : le vrai symbole WILD
					// prend le relais visuellement a cet instant precis.
					hearts[index].alpha = 0;
					resolve();
				}
			};

			requestAnimationFrame(step);
		});

	onMount(() => {
		(async () => {
			await new Promise((r) => setTimeout(r, BASE_DELAY));
			for (let i = 0; i < hearts.length; i++) {
				await flyTo(i);
			}
		})();
	});
</script>

{#each hearts as heart (heart.id)}
	<Container x={heart.x} y={heart.y} alpha={heart.alpha} scale={heart.scale}>
		<Sprite key="heartBullet" anchor={0.5} width={HEART_SIZE} height={HEART_SIZE} />
	</Container>
{/each}
