<script lang="ts">
	import { Container, Sprite } from 'pixi-svelte';

	type Props = {
		filled: number; // 0 a 6
		size?: number; // largeur cible du presentoir en pixels
	};

	const props: Props = $props();

	// ============================================================
	// REGLAGES RAPIDES
	//  - HEART_SIZE_FRAC : taille des coeurs (fraction de la taille du presentoir)
	//  - HEART_NUDGES : decalage fin en UNITES DIRECTES (meme echelle que
	//    size(), pas de conversion mm - valeurs a la taille de reference
	//    130px ; si size() change, les decalages sont mis a l'echelle
	//    proportionnellement)
	//  - REMOVE_STAGGER_MS / REMOVE_DURATION_MS : rythme du retrait des
	//    coeurs un par un (calibre sur le rythme de SuperlikeHeartThrow)
	// ============================================================
	const HEART_SIZE_FRAC = 0.44328;
	const REFERENCE_SIZE = 130;
	const REMOVE_STAGGER_MS = 550;
	const REMOVE_DURATION_MS = 400;

	const IMAGE_ASPECT = 1492 / 1054;

	const HEART_FRACS = [
		{ x: 0.4365, y: 0.2614 }, // haut
		{ x: 0.2182, y: 0.3552 }, // haut-gauche
		{ x: 0.6499, y: 0.3552 }, // haut-droite
		{ x: 0.2182, y: 0.5663 }, // bas-gauche
		{ x: 0.6499, y: 0.5663 }, // bas-droite
		{ x: 0.4365, y: 0.63 }, // bas
	];

	// decalage fin en unites directes (echelle REFERENCE_SIZE=130) : { downUnits, rightUnits }
	const HEART_NUDGES = [
		{ downUnits: 9.5, rightUnits: 7.5 }, // haut
		{ downUnits: 12.5, rightUnits: 3.5 }, // haut-gauche
		{ downUnits: 12.5, rightUnits: 13 }, // haut-droite
		{ downUnits: 12.5, rightUnits: 3.5 }, // bas-gauche
		{ downUnits: 12.5, rightUnits: 14 }, // bas-droite
		{ downUnits: 20.5, rightUnits: 8 }, // bas
	];

	const size = () => props.size ?? REFERENCE_SIZE;
	const height = () => size() * IMAGE_ASPECT;
	const scaleUnit = (u: number) => u * (size() / REFERENCE_SIZE);
	const heartOffset = (i: number) => {
		const frac = HEART_FRACS[i];
		const nudge = HEART_NUDGES[i];
		return {
			x: (frac.x - 0.5) * size() + scaleUnit(nudge.rightUnits),
			y: (frac.y - 0.5) * height() + scaleUnit(nudge.downUnits),
		};
	};

	// Etat d'animation : alpha/echelle de chacun des 6 coeurs, pour les
	// retirer un par un (au lieu d'un saut instantane de tous en meme temps)
	let alphas = $state<number[]>([1, 1, 1, 1, 1, 1]);
	let scales = $state<number[]>([1, 1, 1, 1, 1, 1]);
	let currentTarget = 6;
	let didInit = false;

	const animateFrame = (duration: number, onFrame: (t: number) => void) => {
		const start = performance.now();
		const step = (now: number) => {
			const t = Math.min((now - start) / duration, 1);
			onFrame(t);
			if (t < 1) requestAnimationFrame(step);
		};
		requestAnimationFrame(step);
	};

	$effect(() => {
		const target = Math.max(0, Math.min(Math.round(props.filled), 6));

		if (!didInit) {
			for (let i = 0; i < 6; i++) {
				alphas[i] = i < target ? 1 : 0;
				scales[i] = 1;
			}
			currentTarget = target;
			didInit = true;
			return;
		}

		if (target < currentTarget) {
			const from = currentTarget;
			for (let idx = from - 1; idx >= target; idx--) {
				const delay = (from - 1 - idx) * REMOVE_STAGGER_MS;
				setTimeout(() => {
					animateFrame(REMOVE_DURATION_MS, (t) => {
						alphas[idx] = 1 - t;
						scales[idx] = 1 - t * 0.4;
					});
				}, delay);
			}
			currentTarget = target;
		} else if (target > currentTarget) {
			for (let i = currentTarget; i < target; i++) {
				alphas[i] = 1;
				scales[i] = 1;
			}
			currentTarget = target;
		}
	});
</script>

<Container>
	<Sprite key="afterDarkHeartDisplay" anchor={0.5} width={size()} height={height()} />
	{#each HEART_FRACS as _, i}
		{@const offset = heartOffset(i)}
		<Sprite
			key="heartBullet"
			anchor={0.5}
			x={offset.x}
			y={offset.y}
			width={size() * HEART_SIZE_FRAC * (scales[i] ?? 1)}
			height={size() * HEART_SIZE_FRAC * (scales[i] ?? 1)}
			alpha={alphas[i] ?? 1}
		/>
	{/each}
</Container>
