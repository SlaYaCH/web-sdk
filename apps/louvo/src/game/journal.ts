// ------------------------------------------------------------------
// LE JOURNAL DE BORD.                                     (lot 152)
//
// Quatre lignes partaient dans la console a chaque partie :
//
//     [louvo] personnages : atlas charges
//     [louvo] personnages en place : {...}
//     [louvo] bilan ambiance : {...}
//     [louvo] bilan animations : {...}
//
// Elles ne signalent aucun probleme : elles racontent que tout va
// bien. Elles ont servi a traquer l'ambiance figee, l'ecran noir du
// shader et le montage rate des personnages - a chaque fois ce sont
// elles qui ont donne la reponse.
//
// Dans un jeu fini, c'est du debogage qui traine. On les eteint,
// mais on ne les SUPPRIME PAS : le jour ou quelque chose recommence,
// elles valent de l'or.
//
// POUR LES RALLUMER : JOURNAL = true, puis un build. C'est tout.
//
// Ne passent PAS par ici : les console.warn et console.error. Ils ne
// se declenchent que si quelque chose rate vraiment. Etouffer un
// vrai probleme pour faire propre, c'est se retrouver sans rien le
// jour ou ca casse chez un joueur.
// ------------------------------------------------------------------

export const JOURNAL = false;

/** Un constat de bon fonctionnement. Muet tant que JOURNAL est faux. */
export const dire = (...morceaux: unknown[]) => {
	if (!JOURNAL) return;
	try {
		console.log(...morceaux);
	} catch {
		// une ligne de journal ne doit jamais rien casser
	}
};
