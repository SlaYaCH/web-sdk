<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Graphics, Text } from 'pixi-svelte';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { getSymbolX } from '../game/utils';
	import { SYMBOL_HEIGHT, REEL_PADDING } from '../game/constants';
	import type { PhasesLigne } from '../game/winLineSpeed.svelte';

	type Position = { reel: number; row: number };
	type Props = {
		positions: Position[];
		amount: number;
		/** Les cinq temps de CETTE ligne, calcules par dureesLignes. */
		phases: PhasesLigne;
		oncomplete: () => void;
	};
	const props: Props = $props();

	// ============================================================
	// REGLAGES RAPIDES
	// ============================================================
	const LINE_COLOR = 0xffe14d;
	const LINE_WIDTH = 6;
	const AMOUNT_Y_OFFSET = 40; // au-dessus de LA PROPRE hauteur moyenne de cette ligne
	// Une pastille sur chaque case traversee, dans le MEME jaune et
	// sans aucun contour. Elle dit quelles cases comptent, la ou un
	// simple trait laisse un doute quand deux lignes se croisent.
	const PASTILLES = true; // <<< false pour n'avoir que le trait
	const PASTILLE_RAYON = 9;
	// Les temps ne sont plus calcules ici : ils viennent de
	// dureesLignes(), le calcul commun a WinLinesDisplay et au handler
	// winInfo. Le facteur turbo y est deja applique. Lus une seule
	// fois, a la creation de la ligne.
	const APPARITION_MS = props.phases.apparition;
	const HOLD_MS = props.phases.maintien;
	const LINE_FADE_MS = props.phases.disparitionLigne;
	const AMOUNT_EXTRA_HOLD_MS = props.phases.attenteMontant;
	const AMOUNT_FADE_MS = props.phases.disparitionMontant;

	let lineAlpha = $state(0);
	let amountAlpha = $state(0);

	// Les lignes sont dessinees DANS le conteneur du plateau (voir
	// WinLinesDisplay) : leurs coordonnees doivent donc etre LOCALES, comme
	// celles des symboles. getSymbolY renvoie une position ABSOLUE dans la
	// mise en page ; la melanger avec getSymbolX, qui est locale, donnait un
	// ecart invisible sur bureau mais d'une case entiere en portrait, ou la
	// boite de cadre et l'echelle du plateau ne valent plus 1.
	//
	// On reprend la convention de SuperlikeHeartThrow, validee en jeu (les
	// coeurs tombent pile sur les symboles) :
	//     centre de rangee = SYMBOL_HEIGHT * (rangee + REEL_PADDING)
	const WIN_LINE_Y_OFFSET = 0; // nudge fin, en unites de plateau

	// ------------------------------------------------------------------
	// DECALAGE DE RANGEE.
	// Les lignes de gain tombaient exactement une case trop bas, dans
	// tous les modes. Un ecart constant d'une case, identique partout,
	// n'est pas un probleme de mise en page : c'est que l'indice de
	// rangee fourni par props.positions ne part pas du meme zero que
	// celui des symboles. La formule ci-dessous reste la bonne, on
	// remet juste l'indice dans le bon repere.
	// Mettre 0 pour annuler. Unite : la case.
	// ------------------------------------------------------------------
	const WIN_LINE_ROW_SHIFT = -1;

	const points = props.positions.map((p) => ({
		x: getSymbolX(p.reel),
		y: SYMBOL_HEIGHT * (p.row + WIN_LINE_ROW_SHIFT + REEL_PADDING) + WIN_LINE_Y_OFFSET,
	}));
	// Centre du montant : moyenne des points de CETTE ligne precise (pas un
	// point fixe partage) - deux lignes a des hauteurs differentes affichent
	// donc leur montant a des hauteurs differentes, sans se chevaucher.
	const midX = points.reduce((sum, p) => sum + p.x, 0) / points.length;
	const midY = points.reduce((sum, p) => sum + p.y, 0) / points.length;

	const animate = (duration: number, onFrame: (t: number) => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			const step = (now: number) => {
				const t = Math.min((now - start) / duration, 1);
				onFrame(t);
				if (t < 1) requestAnimationFrame(step);
				else resolve();
			};
			requestAnimationFrame(step);
		});

	onMount(() => {
		(async () => {
			await animate(APPARITION_MS, (t) => {
				lineAlpha = t;
				amountAlpha = t;
			});
			await new Promise((r) => setTimeout(r, HOLD_MS));
			await animate(LINE_FADE_MS, (t) => (lineAlpha = 1 - t));
			await new Promise((r) => setTimeout(r, AMOUNT_EXTRA_HOLD_MS));
			await animate(AMOUNT_FADE_MS, (t) => (amountAlpha = 1 - t));
			props.oncomplete();
		})();
	});
</script>

<Container alpha={lineAlpha} zIndex={40}>
	<Graphics
		draw={(g) => {
			g.moveTo(points[0].x, points[0].y);
			for (let i = 1; i < points.length; i++) {
				g.lineTo(points[i].x, points[i].y);
			}
			g.stroke({ width: LINE_WIDTH, color: LINE_COLOR });
			if (PASTILLES) {
				for (const p of points) {
					g.circle(p.x, p.y, PASTILLE_RAYON).fill({ color: LINE_COLOR });
				}
			}
		}}
	/>
</Container>
<Container x={midX} y={midY - AMOUNT_Y_OFFSET} alpha={amountAlpha} zIndex={40}>
	<Text
		anchor={0.5}
		text={bookEventAmountToCurrencyString(props.amount)}
		style={{
			fontFamily: 'proxima-nova',
			fontWeight: '700',
			fontSize: 32,
			fill: 0xffe14d,
			align: 'center',
			stroke: { color: 0x000000, width: 4 },
		}}
	/>
</Container>
