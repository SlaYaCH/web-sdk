import { stateBet } from 'state-shared';

// ------------------------------------------------------------------
// VITESSE DE PRESENTATION DES LIGNES DE GAIN
//
// Trois endroits doivent rester d'accord, sinon le tour suivant part
// par-dessus une animation inachevee :
//   - WinLineReveal    : l'animation d'une ligne
//   - WinLinesDisplay  : l'ecart entre deux lignes
//   - bookEventHandlerMap (winInfo) : l'attente avant la suite
// Ils lisent tous les trois ce meme facteur.
//
// On ne raccourcit JAMAIS un gain qui atteint au moins BIG WIN : c'est
// le moment que le joueur veut voir.
// ------------------------------------------------------------------

// ==================================================================
// REGLAGES
// ==================================================================
// 1 = vitesse normale. 2.5 = deux fois et demie plus rapide.
const FACTEUR_TURBO = 2.5;
const FACTEUR_SUPER_TURBO = 4;
// ==================================================================

// Pose par le handler winInfo juste avant d'afficher les lignes.
export const stateWinLineSpeed = $state({ atteintBigWin: false });

export const winLineSpeed = () => {
	if (stateWinLineSpeed.atteintBigWin) return 1;
	if (stateBet.isSuperTurbo) return FACTEUR_SUPER_TURBO;
	if (stateBet.isTurbo) return FACTEUR_TURBO;
	return 1;
};

// ------------------------------------------------------------------
// LA CADENCE DES LIGNES                                    (lot 139)
//
// Avant, les lignes s'EMPILAIENT : chacune vivait 1520 ms et la
// suivante partait 200 ms plus tard. Avec cinq gains, cinq lignes et
// cinq montants etaient a l'ecran en meme temps.
//
// Maintenant elles defilent une par une. Quand il y en a beaucoup,
// chacune est raccourcie pour que l'ensemble tienne dans un budget,
// avec un plancher pour qu'aucune ne soit trop breve pour etre lue.
// UNE LIGNE SEULE GARDE EXACTEMENT SON RYTHME D'AVANT.
//
// C'est le SEUL calcul de cadence. Les trois endroits qui doivent
// rester d'accord le lisent tous les trois :
//   - WinLineReveal    : les cinq temps d'une ligne
//   - WinLinesDisplay  : l'ecart entre deux lignes
//   - bookEventHandlerMap (winInfo) : l'attente avant la suite
// Ils ne peuvent donc plus se contredire - c'est le bug du lot 76,
// celui qui ne se voit qu'en turbo.
// ------------------------------------------------------------------

// Les cinq temps d'une ligne a pleine duree. Leur somme fait 1520 ms,
// le rythme d'origine, au millieme pres.
const PHASES_PLEINES = {
	apparition: 120,
	maintien: 700,
	disparitionLigne: 150,
	attenteMontant: 300,
	disparitionMontant: 250,
};
// Les memes, compresses au maximum : en dessous on ne lit plus rien.
const PHASES_MINI = {
	apparition: 60,
	maintien: 180,
	disparitionLigne: 80,
	attenteMontant: 100,
	disparitionMontant: 120,
};
const CLES = [
	'apparition',
	'maintien',
	'disparitionLigne',
	'attenteMontant',
	'disparitionMontant',
] as const;
export type PhasesLigne = Record<(typeof CLES)[number], number>;

// ==================================================================
// REGLAGES
// ==================================================================
const DUREE_PLEINE = 1520; // une ligne seule, rythme d'origine
const BUDGET_MS = 3200; // duree visee quand il y a plusieurs lignes
const PLAFOND_MS = 5200; // au-dela, les lignes se recouvrent un peu
const PLANCHER_MS = 680; // jamais plus court que ca
// Marge de securite sur l'attente finale : la boucle de setTimeout de
// WinLinesDisplay derive de quelques millisecondes par ligne. Sans
// elle, le tour suivant pourrait partir un cheveu trop tot - c'est
// exactement le bug du lot 76.
const MARGE_MS = 120;
// ==================================================================

export const dureesLignes = (nombre: number) => {
	const n = Math.max(1, nombre);
	const vitesse = winLineSpeed();
	const brut =
		n === 1
			? DUREE_PLEINE
			: Math.max(PLANCHER_MS, Math.min(DUREE_PLEINE, BUDGET_MS / n));
	const k = brut / DUREE_PLEINE;
	const phases = {} as PhasesLigne;
	let duree = 0;
	for (const cle of CLES) {
		const v = Math.max(PHASES_MINI[cle], PHASES_PLEINES[cle] * k);
		phases[cle] = v / vitesse;
		duree += v;
	}
	duree = duree / vitesse;
	// L'ecart vaut la duree d'une ligne : la suivante part quand la
	// precedente s'efface. Il ne se resserre que s'il y a tellement de
	// lignes que la sequence deborderait du plafond.
	const ecart = Math.min(duree, PLAFOND_MS / n / vitesse);
	return {
		phases,
		duree,
		ecart,
		total: ecart * (n - 1) + duree + MARGE_MS / vitesse,
		vitesse,
		nombre: n,
	};
};
