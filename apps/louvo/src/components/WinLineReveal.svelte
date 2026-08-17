<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Graphics, Text } from 'pixi-svelte';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { getSymbolX, getSymbolY } from '../game/utils';

	type Position = { reel: number; row: number };
	type Props = {
		positions: Position[];
		amount: number;
		oncomplete: () => void;
	};
	const props: Props = $props();

	// ============================================================
	// REGLAGES RAPIDES
	// ============================================================
	const LINE_COLOR = 0xffe14d;
	const LINE_WIDTH = 6;
	const AMOUNT_Y_OFFSET = 40; // au-dessus de LA PROPRE hauteur moyenne de cette ligne
	const HOLD_MS = 700;
	const LINE_FADE_MS = 150;
	const AMOUNT_EXTRA_HOLD_MS = 300;
	const AMOUNT_FADE_MS = 250;

	let lineAlpha = $state(0);
	let amountAlpha = $state(0);

	const points = props.positions.map((p) => {
		const rawIndex = p.row - 1;
		// Pour la rangee du haut (row=0), rawIndex vaut -1 : on extrapole sa
		// position en reculant d'un ecart de rangee depuis l'indice 0, au
		// lieu de bloquer sur l'indice 0 (ce qui la confondait avec la
		// rangee suivante).
		const rowGap = getSymbolY(1) - getSymbolY(0);
		const y = rawIndex >= 0 ? getSymbolY(rawIndex) - 18 : getSymbolY(0) - rowGap - 18;
		return {
			x: getSymbolX(p.reel),
			y,
		};
	});
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
			await animate(120, (t) => {
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

<Container alpha={lineAlpha}>
	<Graphics
		draw={(g) => {
			g.moveTo(points[0].x, points[0].y);
			for (let i = 1; i < points.length; i++) {
				g.lineTo(points[i].x, points[i].y);
			}
			g.stroke({ width: LINE_WIDTH, color: LINE_COLOR });
		}}
	/>
</Container>
<Container x={midX} y={midY - AMOUNT_Y_OFFSET} alpha={amountAlpha}>
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
