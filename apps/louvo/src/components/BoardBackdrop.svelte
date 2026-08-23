<script lang="ts">
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { boardBox } from '../game/boardBox';

	// ------------------------------------------------------------------
	// FOND NOIR DERRIERE LA GRILLE
	//
	// Depuis que le decor est une image pleine, les parties transparentes
	// des symboles laissent voir la scene au travers - visible surtout sur
	// les wilds, dont les bords sont decoupes. Avant, le fond contenait la
	// grille et faisait ecran.
	//
	// LES DEUX CADRES N'ONT PAS LA MEME GRILLE.
	// Mesure faite sur les images : chaque cadre contient 25 trous
	// transparents, un par case. L'union de ces trous donne la grille
	// reelle. After Dark est 52 px plus large que la base, et pas centree
	// pareil. C'est pour ca que cet aplat a ses PROPRES mesures au lieu de
	// reutiliser GRID_FRACS, qui contient les memes chiffres pour les deux
	// paliers depuis qu'on a aligne le placement des symboles.
	//
	// LE DEBORD AUSSI EST PROPRE A CHAQUE PALIER.
	// Le cadre est dessine par-dessus, donc le debord ne se voit pas -
	// tant qu'il reste sous le cadre. Aux quatre coins l'ouverture est
	// arrondie : un rectangle ne peut pas s'y inscrire aussi loin
	// qu'ailleurs. Plafond mesure avant que les coins ne depassent :
	// 28 px en base, 30 px en After Dark. On garde de la marge.
	// Le minimum utile est d'environ 4 px, ce dont les symboles
	// depassent leur case.
	// ------------------------------------------------------------------

	// ==================================================================
	// MESURES, en pixels des images 1672 x 941
	// board_frame_overlay.png et board_frame_overlay_after_dark.png
	// ==================================================================
	const TROU = {
		base: { left: 495, right: 1162, top: 134, bottom: 653, debord: 18 },
		afterDark: { left: 471, right: 1190, top: 136, bottom: 662, debord: 24 },
	} as const;

	// Opacite de l'aplat. 1 = noir franc.
	const OPACITE = 1;
	// ==================================================================

	const IMAGE_LARGEUR = 1672;
	const IMAGE_HAUTEUR = 941;

	const context = getContext();

	const box = $derived(boardBox(context.stateGame.tier));
	const trou = $derived(context.stateGame.tier === 'after_dark' ? TROU.afterDark : TROU.base);

	const zone = $derived({
		x: box.x + (box.width * (trou.left - trou.debord)) / IMAGE_LARGEUR,
		y: box.y + (box.height * (trou.top - trou.debord)) / IMAGE_HAUTEUR,
		width: (box.width * (trou.right - trou.left + trou.debord * 2)) / IMAGE_LARGEUR,
		height: (box.height * (trou.bottom - trou.top + trou.debord * 2)) / IMAGE_HAUTEUR,
	});
</script>

<Rectangle {...zone} backgroundColor={0x000000} backgroundAlpha={OPACITE} zIndex={-1} />
