<script lang="ts">
	// ============================================================
	// LE GESTE DU CLIC, EN SURIMPRESSION.               (lot 136)
	//
	// Les boutons de la barre sont PEINTS DANS bottom_bar.webp : le
	// code ne contient que des rectangles invisibles poses par
	// dessus. Il n'y a donc aucun sprite a faire rentrer sous le
	// doigt - enfoncer un rectangle invisible ne se voit pas.
	//
	// Ce composant se pose DANS la zone cliquable et dessine, par
	// dessus votre image, trois choses qui ne se voient que pendant
	// le geste :
	//
	//     un halo      quand la souris survole
	//     un voile     quand le doigt appuie : le bouton rentre
	//     une onde     quand l'action part pour de bon
	//
	// Plus un voile permanent quand le bouton est eteint, ce que la
	// barre ne montrait pas du tout jusqu'ici.
	//
	// Au repos, tout est a alpha 0 : votre visuel est intact.
	//
	// Pixi brut monte dans pixi-svelte, comme pour les symboles et
	// l'ambiance - le procede est deja eprouve dans ce jeu.
	// ============================================================
	import { onDestroy } from 'svelte';
	import { getContextParent } from 'pixi-svelte';
	import { Container, Graphics } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	type Props = {
		/** Taille de la zone, en coordonnees de la barre. */
		largeur: number;
		hauteur: number;
		/** Bouton rond (SPIN, AUTOPLAY) plutot que rectangle arrondi. */
		cercle?: boolean;
		/** Teinte du halo et de l'onde. */
		couleur?: number;
		/** La souris est-elle dessus ? */
		survole?: boolean;
		/** Le doigt est-il appuye ? */
		presse?: boolean;
		/** false = bouton eteint : voile permanent, aucun effet. */
		actif?: boolean;
		/** Compteur incremente a chaque action reelle : lance l'onde. */
		coup?: number;
		/** Voile de l'etat eteint. 0 pour les boutons qui se
		 *  decolorent deja tout seuls via alpha. */
		voileEteint?: number;
	};
	const props: Props = $props();

	// --- LES REGLAGES ---
	const COULEUR_DEFAUT = 0xff2d6a; // le rose de Louvo
	const HALO_SURVOL = 0.22; // la lueur au survol
	const HALO_APPUI = 0.1; // elle baisse quand on enfonce
	const VOILE_APPUI = 0.3; // a quel point le bouton rentre
	const VOILE_ETEINT = 0.32; // a quel point un bouton eteint s'efface
	const ONDE_MS = 340; // la duree de l'onde
	const ONDE_ALPHA = 0.6;

	const couleur = props.couleur ?? COULEUR_DEFAUT;
	const demiL = props.largeur * 0.5;
	const demiH = props.hauteur * 0.5;
	const coin = Math.min(demiL, demiH) * 0.35;

	const parentContext = getContextParent();

	// La forme de la zone, a l'echelle demandee.
	const forme = (g: Graphics, k: number) => {
		if (props.cercle) return g.ellipse(0, 0, demiL * k, demiH * k);
		return g.roundRect(
			-demiL * k,
			-demiH * k,
			props.largeur * k,
			props.hauteur * k,
			coin * k,
		);
	};

	const racine = new Container();
	racine.eventMode = 'none'; // ne vole jamais un clic

	// Le voile : un aplat sombre qui donne le creux.
	const voile = new Graphics();
	forme(voile, 1).fill({ color: 0x000000, alpha: 1 });
	voile.alpha = 0;

	// Le halo : des couches concentriques, pour un degrade doux.
	const halo = new Graphics();
	for (let i = 1; i <= 8; i += 1) {
		forme(halo, 0.7 + i * 0.08).fill({ color: couleur, alpha: 0.075 });
	}
	halo.blendMode = 'add';
	halo.alpha = 0;

	// L'onde : un contour qui s'ecarte et se dissipe.
	const onde = new Graphics();
	forme(onde, 1).stroke({
		color: couleur,
		width: Math.max(2, Math.min(demiL, demiH) * 0.09),
		alpha: 1,
	});
	onde.blendMode = 'add';
	onde.alpha = 0;

	racine.addChild(voile, halo, onde);
	parentContext.addToParent(racine);

	// --- Les mouvements ---
	const haloTween = new Tween(0, { duration: 140, easing: cubicOut });
	const voileTween = new Tween(0, { duration: 90, easing: cubicOut });
	const ondeTween = new Tween(1, { duration: 0 });

	const eteint = $derived(props.actif === false);

	$effect(() => {
		if (eteint) {
			haloTween.set(0);
			voileTween.set(props.voileEteint ?? VOILE_ETEINT, { duration: 200 });
			return;
		}
		haloTween.set(
			props.presse ? HALO_APPUI : props.survole ? HALO_SURVOL : 0,
		);
		voileTween.set(props.presse ? VOILE_APPUI : 0);
	});

	$effect(() => {
		halo.alpha = haloTween.current;
		voile.alpha = voileTween.current;
	});

	// L'onde ne part QUE sur un coup reel : le gestionnaire
	// l'incremente apres ses garde-fous. Un bouton eteint ne
	// clignote donc jamais pour rien, et la barre Espace anime le
	// bouton exactement comme la souris.
	let dernierCoup = props.coup ?? 0;
	$effect(() => {
		const coup = props.coup ?? 0;
		if (coup === dernierCoup) return;
		dernierCoup = coup;
		if (eteint) return;
		ondeTween.set(0, { duration: 0 });
		ondeTween.set(1, { duration: ONDE_MS, easing: cubicOut });
	});

	$effect(() => {
		const t = ondeTween.current;
		onde.alpha = t >= 1 ? 0 : (1 - t) * ONDE_ALPHA;
		const k = 0.55 + t * 0.95;
		onde.scale.set(k);
	});

	onDestroy(() => {
		try {
			racine.destroy({ children: true });
		} catch {
			/* on nettoie au mieux */
		}
	});
</script>
