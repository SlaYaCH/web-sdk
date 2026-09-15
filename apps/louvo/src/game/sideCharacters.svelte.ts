import { stateBet, stateUi } from 'state-shared';
import { API_AMOUNT_MULTIPLIER } from 'constants-shared/bet';

// ------------------------------------------------------------------
// LE PONT VERS LES PERSONNAGES LATERAUX.                  (lot 147)
//
// Le composant LouvoSideCharacters branche le duo et son directeur
// ici. Le reste du jeu n'appelle que les deux fonctions du bas, et
// ne sait rien du reste.
//
// Tant que rien n'est branche - personnages eteints, mobile, atlas
// pas encore charges - les deux fonctions ne font rien du tout.
//
// TOUT EST SOUS try/catch. Une decoration ne doit JAMAIS pouvoir
// interrompre un tour qui engage de l'argent. Meme principe que
// recordRound.
// ------------------------------------------------------------------

let duo: any = null;
let directeur: any = null;
let horloge: () => number = () => 0;
let compteurBonus = 0;
let tracer = false;

export const brancherPersonnages = (
	d: any,
	dir: any,
	h: () => number,
	t = false,
) => {
	duo = d;
	directeur = dir;
	horloge = h;
	tracer = t;
};

export const debrancherPersonnages = () => {
	duo = null;
	directeur = null;
	horloge = () => 0;
	tracer = false;
};

// Le directeur renvoie a chaque fois la RAISON de sa decision :
//   reaction               ils ont joue quelque chose
//   small-win-idle         gain trop petit pour le seuil
//   win-cooldown           trop tot apres la reaction precedente
//   no-win-idle            tour sans gain, rien a dire
//   streak-already-reacted l'agacement a deja ete joue
//   duplicate              ce tour a deja ete compte
// Sans ca, un tour sans reaction est indistinguable d'une panne.
const dire = (quoi: string, bilan: any, extra: any = {}) => {
	if (!tracer) return;
	try {
		console.log(
			'[louvo] personnages ' + quoi + ' : ' +
				JSON.stringify({ ...extra, ...bilan }),
		);
	} catch {
		// tant pis
	}
};

/**
 * UN SEUL APPEL PAR TOUR, une fois le tour entierement joue.
 * Jamais par ligne gagnante, par coeur ou par tour gratuit : le
 * directeur attend le paiement FINAL agrege.
 */
export const signalerTour = (bet: unknown) => {
	try {
		if (!directeur) return;
		// En replay, la presentation doit etre reproductible : le
		// directeur tire au hasard, on le laisse donc de cote.
		if (stateUi.config.mode === 'replay') return;

		const brut = bet as {
			betID?: number | string;
			roundID?: number | string;
			amount?: number;
			payout?: number;
			payoutMultiplier?: number;
		};

		const id = String(brut?.betID ?? brut?.roundID ?? '');
		if (!id) return;

		// Meme calcul que l'historique, pour ne pas avoir deux
		// verites sur le meme tour.
		const mise =
			typeof brut?.amount === 'number' && brut.amount > 0
				? brut.amount / API_AMOUNT_MULTIPLIER
				: stateBet.wageredBetAmount;
		const paye =
			typeof brut?.payout === 'number' ? brut.payout / API_AMOUNT_MULTIPLIER : null;
		const multiplicateur =
			typeof brut?.payoutMultiplier === 'number'
				? brut.payoutMultiplier
				: paye !== null && mise > 0
					? paye / mise
					: 0;

		if (!Number.isFinite(multiplicateur) || multiplicateur < 0) return;

		const bilan = directeur.onRound({
			roundId: id,
			payoutMultiplier: multiplicateur,
			nowMs: horloge(),
		});
		dire('tour', bilan, { gain: Number(multiplicateur.toFixed(2)) + 'x' });
	} catch (erreur) {
		console.warn('[louvo] personnages : tour ignore', erreur);
	}
};

/** A l'entree en bonus, avant que la transition ne masque la scene. */
export const signalerBonus = () => {
	try {
		if (!directeur) return;
		if (stateUi.config.mode === 'replay') return;
		compteurBonus += 1;
		const bilan = directeur.onBonus({
			eventId: 'fs-' + compteurBonus,
			nowMs: horloge(),
		});
		dire('bonus', bilan);
	} catch (erreur) {
		console.warn('[louvo] personnages : bonus ignore', erreur);
	}
};
