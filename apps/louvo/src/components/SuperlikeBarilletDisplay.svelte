<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';
	import { getContext } from '../game/context';

	type Props = {
		likes: number; // 1 a 6
	};
	const props: Props = $props();
	const context = getContext();

	// ============================================================
	// REGLAGES RAPIDES - si le positionnement n'est toujours pas
	// exact, ce sont les 2 seules valeurs a retoucher (comme pour
	// l'alignement de la grille principale) :
	//  - HUB_Y : fait monter (valeur plus petite) ou descendre
	//    (valeur plus grande) tout le groupe de coeurs en meme temps.
	//  - HEART_SIZE / CENTER_HEART_SIZE : taille des coeurs.
	// Sauver le fichier + redemarrage complet suffit pour voir l'effet.
	const HUB_Y = 155;
	const HEART_SIZE = 55;
	const CENTER_HEART_SIZE = 26;
	// ============================================================

	const HUB = { x: 0, y: HUB_Y };
	const OUTER_HEARTS = [
		{ x: 0, y: -41.3 },
		{ x: -24.8, y: -19.8 },
		{ x: 24.8, y: -19.8 },
		{ x: -24.8, y: 20.6 },
		{ x: 24.8, y: 20.6 },
		{ x: 0, y: 41.3 },
	];

	const filledCount = Math.max(0, Math.min(Math.round(props.likes), 6));

	let centerScale = $state(0);
	let outerScales = $state<number[]>(Array(filledCount).fill(0));
	let outerAlphas = $state<number[]>(Array(filledCount).fill(1));

	const easeOutBack = (t: number) => {
		const c1 = 1.70158;
		const c3 = c1 + 1;
		return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
	};

	const animate = (duration: number, delay: number, onFrame: (t: number) => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now() + delay;
			const step = (now: number) => {
				const elapsed = now - start;
				if (elapsed < 0) {
					requestAnimationFrame(step);
					return;
				}
				const t = Math.min(elapsed / duration, 1);
				onFrame(t);
				if (t < 1) requestAnimationFrame(step);
				else resolve();
			};
			requestAnimationFrame(step);
		});

	onMount(() => {
		animate(180, 80, (t) => (centerScale = easeOutBack(t)));

		for (let i = 0; i < filledCount; i++) {
			animate(180, 120 + i * 25, (t) => (outerScales[i] = easeOutBack(t)));
		}
	});

	// Vide le presentoir au rythme REEL des lancers (synchronise via
	// stateGame.superlikeHeartsLaunched, mis a jour par SuperlikeHeartThrow),
	// au lieu d'un minuteur fixe decorrele du vrai depart des coeurs.
	const vanished = new Set<number>();
	$effect(() => {
		const launched = context.stateGame.superlikeHeartsLaunched;
		for (let i = 0; i < Math.min(launched, filledCount); i++) {
			if (vanished.has(i)) continue;
			vanished.add(i);
			animate(200, 0, (t) => {
				outerAlphas[i] = 1 - t;
				outerScales[i] = 1 - t * 0.4;
			});
		}
	});
</script>

<Container x={HUB.x} y={HUB.y} scale={centerScale}>
	<Sprite key="heartBullet" anchor={0.5} width={CENTER_HEART_SIZE} height={CENTER_HEART_SIZE} />
</Container>

<Container x={HUB.x} y={HUB.y}>
	{#each OUTER_HEARTS.slice(0, filledCount) as heart, i}
		<Container x={heart.x} y={heart.y} scale={outerScales[i] ?? 0} alpha={outerAlphas[i] ?? 1}>
			<Sprite key="heartBullet" anchor={0.5} width={HEART_SIZE} height={HEART_SIZE} />
		</Container>
	{/each}
</Container>
