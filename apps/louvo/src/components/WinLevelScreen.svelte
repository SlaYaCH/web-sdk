<script lang="ts">
	// ============================================================
	// L'ecran de palier : l'image du palier et le montant qui monte.
	//
	// Tout est ici, y compris le montant : un seul fichier a ouvrir
	// pour regler cet ecran, et rien a chercher ailleurs.
	// ============================================================
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { ResponsiveBitmapText } from 'components-pixi';
	import { stateBetDerived } from 'state-shared';

	import { SYMBOL_SIZE } from '../game/constants';

	type Props = { alias: string; montant: string };
	const props: Props = $props();

	// =====================================================
	//  BIG / SUPER / MEGA / EPIC WIN  -  vos quatre images
	// =====================================================
	const TAILLE = 1 / 3; // <<< LA taille de l'image. 1 = comme avant.
	const IMAGE_Y = -SYMBOL_SIZE * 0.55; // hauteur de l'image
	const MONTANT_Y = SYMBOL_SIZE * 0.95; // hauteur du montant
	const MONTANT_TAILLE = SYMBOL_SIZE * 0.75; // taille des chiffres
	const MONTANT_LARGEUR = SYMBOL_SIZE * 3.4; // au-dela, le texte retrecit
	const FOND_LARGEUR = SYMBOL_SIZE * 3.8; // le rectangle noir
	const FOND_HAUTEUR = SYMBOL_SIZE * 1.0;
	const FOND_OPACITE = 0.6; // 0 = pas de fond noir du tout

	// =====================================================
	//  MAX WIN  -  n'a jamais utilise le spine, ne bouge pas
	// =====================================================
	const MAX_IMAGE_Y = -SYMBOL_SIZE * 0.5;
	const MAX_MONTANT_Y = SYMBOL_SIZE * 2.15;
	const MAX_MONTANT_TAILLE = SYMBOL_SIZE * 0.68;
	const MAX_MONTANT_LARGEUR = SYMBOL_SIZE * 3.4;

	// Votre cadre derriere le montant du MAX WIN : le meme sprite que
	// le panneau sous la grille et que le total de fin de bonus.
	const MAX_CADRE = true; // <<< false pour un montant nu, comme avant
	const MAX_CADRE_LARGEUR = SYMBOL_SIZE * 4.2; // <<< LA taille du cadre
	const MAX_CADRE_RATIO = 1536 / 1024; // proportions de l'image, a ne pas deformer
	// Le rose se lisait mal sur le bois fonce du cadre. 0xff2d6a pour
	// le retrouver.
	const MAX_MONTANT_COULEUR = 0xffffff;

	// --- l'animation d'entree ---
	const ENTREE_MS = 420; // duree du surgissement
	const ECHELLE_DEPART = 0.62; // taille de depart
	const RESPIRATION = 0.018; // souffle continu, 0 pour le couper
	const PERIODE_MS = 2600;

	// --- les proportions d'origine de l'ecran, avant reduction ---
	const LARGEUR_PLEINE = SYMBOL_SIZE * 6.6;
	const HAUTEUR_PLEINE = SYMBOL_SIZE * 4.4;

	const CLE_ECRAN = {
		big: 'bigwinScreen',
		superwin: 'superwinScreen',
		mega: 'megawinScreen',
		epic: 'epicwinScreen',
		max: 'maxwinScreen',
	} as const;

	const cle = $derived(CLE_ECRAN[props.alias as keyof typeof CLE_ECRAN]);
	const estMax = $derived(props.alias === 'max');

	const largeur = $derived(estMax ? LARGEUR_PLEINE : LARGEUR_PLEINE * TAILLE);
	const hauteur = $derived(estMax ? HAUTEUR_PLEINE : HAUTEUR_PLEINE * TAILLE);
	const imageY = $derived(estMax ? MAX_IMAGE_Y : IMAGE_Y);
	const montantY = $derived(estMax ? MAX_MONTANT_Y : MONTANT_Y);
	const montantTaille = $derived(estMax ? MAX_MONTANT_TAILLE : MONTANT_TAILLE);
	const montantLargeur = $derived(estMax ? MAX_MONTANT_LARGEUR : MONTANT_LARGEUR);
	const montantCouleur = $derived(estMax ? MAX_MONTANT_COULEUR : 0xff2d6a);

	let echelle = $state(ECHELLE_DEPART);

	$effect(() => {
		let arrete = false;
		let precedent = performance.now();
		let horloge = 0;

		const image = (maintenant: number) => {
			if (arrete) return;

			// Le turbo accelere la mise en scene : on suit la meme horloge
			// que le reste du jeu plutot que le temps reel.
			const vitesse = stateBetDerived.timeScale();
			horloge += (maintenant - precedent) * (vitesse > 0 ? vitesse : 1);
			precedent = maintenant;

			const t = Math.min(1, horloge / ENTREE_MS);
			const adouci = 1 - Math.pow(1 - t, 3);
			const souffle =
				t >= 1
					? Math.sin(((horloge - ENTREE_MS) / PERIODE_MS) * Math.PI * 2) * RESPIRATION
					: 0;

			echelle = ECHELLE_DEPART + (1 - ECHELLE_DEPART) * adouci + souffle;

			requestAnimationFrame(image);
		};

		requestAnimationFrame(image);
		return () => {
			arrete = true;
		};
	});
</script>

{#if cle}
	<Sprite
		anchor={0.5}
		key={cle}
		y={imageY}
		width={largeur * echelle}
		height={hauteur * echelle}
	/>

	{#if estMax && MAX_CADRE}
		<!-- Le cadre du MAX WIN. L'image du palier s'arrete au-dessus
			du montant : sans lui, les chiffres flottent sur le decor.
			Il se place AVANT le texte pour passer dessous. -->
		<Sprite
			anchor={0.5}
			key="totalWinFrame"
			y={MAX_MONTANT_Y}
			width={MAX_CADRE_LARGEUR}
			height={MAX_CADRE_LARGEUR / MAX_CADRE_RATIO}
		/>
	{/if}

	{#if !estMax && FOND_OPACITE > 0}
		<!-- Le fond noir derriere le montant. MAX WIN n'en a jamais eu :
			son image occupe tout l'ecran, un rectangle par-dessus ferait
			une tache. -->
		<Rectangle
			anchor={0.5}
			y={MONTANT_Y}
			width={FOND_LARGEUR}
			height={FOND_HAUTEUR}
			backgroundColor={0x000000}
			alpha={FOND_OPACITE}
		/>
	{/if}

	<ResponsiveBitmapText
		anchor={0.5}
		y={montantY}
		maxWidth={montantLargeur}
		text={props.montant}
		style={{
			fontFamily: 'gold', fill: montantCouleur,
			fontSize: montantTaille,
			align: 'center',
			fontWeight: 'bold',
			letterSpacing: 0,
		}}
	/>
{/if}
