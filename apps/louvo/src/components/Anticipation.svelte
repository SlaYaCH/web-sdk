<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Rectangle, Sprite } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import { getContext } from '../game/context';
	import type { Reel } from '../game/stateGame.svelte';
	import { boardBox, gridFracs } from '../game/boardBox';

	type Props = {
		reel: Reel;
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// ============================================================
	// L'ANTICIPATION DE LOUVO
	//
	// Remplace le spine `anticipation`, qui venait du jeu d'exemple du
	// web-sdk et que la regle d'approbation interdit. Tout est dessine
	// en code : un cadre qui pulse, des coeurs qui tombent le long de
	// la colonne. Le seul asset utilise est le coeur des Super Like,
	// que le jeu charge deja.
	//
	// REGLAGES A AJUSTER A L'OEIL
	// ============================================================
	// Le cadre autour de la colonne. 1.0 = exactement la colonne.
	const ANTICIPATION_LARGEUR = 1.0;
	const ANTICIPATION_HAUTEUR = 1.06;

	const COULEUR_CADRE = 0xffd166; // le dore du cadre de la grille
	const COULEUR_HALO = 0xff2d6a; // le rose de Louvo
	const EPAISSEUR_CADRE = 4;
	const HALO_MIN = 0.06; // opacité du halo au creux de la pulsation
	const HALO_MAX = 0.2; // et à son sommet
	const PULSATION_MS = 900; // durée d'un battement

	// Les coeurs qui tombent.
	const NOMBRE_COEURS = 14;
	const CHUTE_MS_RAPIDE = 1100; // temps de traversée du plus rapide
	const CHUTE_MS_LENTE = 2200; // et du plus lent
	const TAILLE_MIN = 0.1; // en fraction de la largeur de colonne
	const TAILLE_MAX = 0.26;
	const ETALEMENT = 0.62; // largeur occupée, en fraction de la colonne
	const BALANCEMENT = 0.1; // amplitude du va-et-vient latéral

	// Fondus.
	const ENTREE_MS = 250;
	const SORTIE_MS = 300;

	// Filet de sécurité : si le rouleau ne se déclare jamais arrêté,
	// l'animation sort d'elle-même au lieu de tourner indéfiniment.
	// C'est ce qui laissait autrefois le drapeau `anticipating` bloqué.
	const DUREE_MAX_MS = 12000;
	// ============================================================

	// Même colonne = même chute à chaque tour. Un tirage aléatoire
	// donnerait un scintillement d'un tour à l'autre.
	const semis = (n: number) => {
		const x = Math.sin(n * 12.9898 + (props.reel.reelIndex + 1) * 78.233) * 43758.5453;
		return x - Math.floor(x);
	};

	const coeurs = Array.from({ length: NOMBRE_COEURS }, (_, i) => ({
		depart: semis(i * 3 + 1),
		duree: CHUTE_MS_RAPIDE + semis(i * 3 + 2) * (CHUTE_MS_LENTE - CHUTE_MS_RAPIDE),
		taille: TAILLE_MIN + semis(i * 3 + 3) * (TAILLE_MAX - TAILLE_MIN),
		colonne: semis(i * 7 + 5) - 0.5,
		oscillation: semis(i * 7 + 6) * Math.PI * 2,
	}));

	let temps = $state(0);
	let opacite = $state(0);
	let termine = false;

	onMount(() => {
		let image: number | null = null;
		const debut = performance.now();
		let debutSortie: number | null = null;

		const boucle = (maintenant: number) => {
			const echelle = stateBetDerived.timeScale();
			const ecoule = (maintenant - debut) * echelle;
			temps = ecoule;

			const doitSortir =
				props.reel.reelState.motion === 'stopped' || ecoule > DUREE_MAX_MS;
			if (doitSortir && debutSortie === null) debutSortie = maintenant;

			if (debutSortie === null) {
				opacite = Math.min(1, ecoule / ENTREE_MS);
			} else {
				const t = ((maintenant - debutSortie) * echelle) / SORTIE_MS;
				opacite = Math.max(0, 1 - t);
				if (t >= 1) {
					if (!termine) {
						termine = true;
						props.oncomplete();
					}
					return;
				}
			}
			image = requestAnimationFrame(boucle);
		};

		image = requestAnimationFrame(boucle);
		return () => {
			if (image !== null) cancelAnimationFrame(image);
		};
	});

	const box = $derived(boardBox(context.stateGame.tier));
	const f = $derived(gridFracs(context.stateGame.tier));
	const largeurColonne = $derived(((f.right - f.left) / 5) * box.width);
	const hauteurGrille = $derived((f.bottom - f.top) * box.height);
	const centreGrilleY = $derived(box.y + box.height * ((f.top + f.bottom) / 2));
	const centreColonne = $derived(
		box.x + box.width * f.left + largeurColonne * (props.reel.reelIndex + 0.5),
	);

	const largeurZone = $derived(largeurColonne * ANTICIPATION_LARGEUR);
	const hauteurZone = $derived(hauteurGrille * ANTICIPATION_HAUTEUR);
	const hautZone = $derived(centreGrilleY - hauteurZone / 2);

	const halo = $derived(
		HALO_MIN +
			(HALO_MAX - HALO_MIN) * (0.5 + 0.5 * Math.sin((temps / PULSATION_MS) * Math.PI * 2)),
	);

	// Chaque coeur avance de 0 a 1 le long de la colonne, puis repart en
	// haut. Il apparait et disparait en fondu a ses deux extremites, donc
	// on ne le voit jamais surgir ni se couper net.
	const chute = $derived(
		coeurs.map((c) => {
			const avance = (c.depart + temps / c.duree) % 1;
			return {
				x:
					c.colonne * largeurZone * ETALEMENT +
					Math.sin(c.oscillation + avance * Math.PI * 4) * largeurZone * BALANCEMENT,
				y: hautZone + avance * hauteurZone,
				taille: largeurZone * c.taille,
				alpha: Math.min(1, Math.sin(avance * Math.PI) * 1.8),
			};
		}),
	);
</script>

<Container x={centreColonne} y={centreGrilleY} alpha={opacite} zIndex={20}>
	<Rectangle
		anchor={0.5}
		width={largeurZone}
		height={hauteurZone}
		backgroundColor={COULEUR_HALO}
		backgroundAlpha={halo}
		borderColor={COULEUR_CADRE}
		borderWidth={EPAISSEUR_CADRE}
	/>
</Container>

<Container x={centreColonne} alpha={opacite} zIndex={21}>
	{#each chute as coeur, i (i)}
		<Container x={coeur.x} y={coeur.y} alpha={coeur.alpha}>
			<Sprite key="heartBullet" anchor={0.5} width={coeur.taille} height={coeur.taille} />
		</Container>
	{/each}
</Container>
