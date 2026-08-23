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
