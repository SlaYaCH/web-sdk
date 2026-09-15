import { i18n, type Messages } from '@lingui/core';
import { type Language } from './stateUrl.svelte';

export const stateI18n = $state({
	i18n
});

// ------------------------------------------------------------------
// LE COMPILATEUR DE MESSAGES.                            (lot 151)
//
// Lingui 5 ne compile plus les catalogues a la volee. Dans son _() :
//
//     let translation = messageForId || message || id;
//     if (isString(translation)) {
//       if (this._messageCompiler) translation = this._messageCompiler(translation);
//       else console.warn('Uncompiled message detected! ...');
//     }
//
// Nos catalogues sont des chaines simples - HOME: 'HOME' - donc
// translation est TOUJOURS une chaine, donc sans compilateur il
// ecrit un avertissement A CHAQUE AFFICHAGE de chaque texte. Seize
// lignes, chacune avec sa trace d'appel, rien que pour le panneau
// d'autoplay.
//
// Cet avertissement n'a PAS de garde-fou de production : il sort
// aussi dans le build livre. Ce n'est donc pas un bruit de
// developpement qu'on pourrait ignorer.
//
// On lui donne donc le compilateur le plus simple possible : celui
// qui rend la chaine telle quelle. Relisez le code ci-dessus -
// translation vaut exactement la meme chose qu'avant, la suite du
// traitement est identique, seul l'avertissement disparait.
//
// Le jour ou les catalogues porteront de vraies regles ICU
// (pluriels, interpolation), il faudra le vrai compilateur de
// Lingui a la place. Aucun texte du jeu n'en contient aujourd'hui.
// ------------------------------------------------------------------
const compilateurNeutre = (message: string) => message;
try {
	const moteur = stateI18n.i18n as unknown as {
		_messageCompiler?: (message: string) => unknown;
	};
	if (!moteur._messageCompiler) moteur._messageCompiler = compilateurNeutre;
} catch (erreur) {
	console.warn('i18n: could not set the message compiler', erreur);
}

export const stateI18nDerived = {
	init: (lang: Language, messages: Messages) => {
		stateI18n.i18n.load(lang, messages as Messages);
		stateI18n.i18n.activate(lang);
	},
	translate: (value: string) => stateI18n.i18n._(stateI18n.i18n.t(value)),
};