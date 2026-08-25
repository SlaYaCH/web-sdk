import { stateUrlDerived } from 'state-shared';

/**
 * Le vocabulaire impose par stake.us.
 *
 * Source : approval_Guideline_complet.txt, "Jurisdiction Requirements".
 * Les Etats-Unis interdisent le vocabulaire du pari dans un casino
 * social : on n'y mise pas, on y joue. Stake fournit la table des
 * remplacements et le drapeau social=true/false dans l'URL.
 *
 * Regle de securite : quand le jeu n'est PAS en mode social, les deux
 * fonctions renvoient leur argument sans y toucher. Le jeu Stake.com
 * est donc strictement inchange par ce fichier.
 *
 * "stake" est volontairement absent de la table : le disclaimer
 * officiel se termine par "TM et (c) 2026 Stake Engine", qui est une
 * marque et non un terme de pari.
 */

// Les expressions longues d'abord : "total bet" doit etre reconnu
// avant "bet", sinon on obtiendrait "total play" par accident au
// mauvais endroit.
const TABLE: [RegExp, string][] = [
	[/\bplace your bets\b/gi, 'come and play'],
	[/\bat the cost of\b/gi, 'for'],
	[/\bwin feature\b/gi, 'play feature'],
	[/\bbonus buys\b/gi, 'bonus plays'],
	[/\bbonus buy\b/gi, 'bonus'],
	[/\bbuy bonus\b/gi, 'get bonus'],
	[/\btotal bet\b/gi, 'total play'],
	[/\bpaid out\b/gi, 'won'],
	[/\bpays out\b/gi, 'won'],
	[/\bpay out\b/gi, 'won'],
	[/\bcost of\b/gi, 'can be played for'],
	[/\bpurchases\b/gi, 'plays'],
	[/\bpurchase\b/gi, 'play'],
	[/\bbetting\b/gi, 'playing'],
	[/\bwithdraw\b/gi, 'redeem'],
	[/\bcurrency\b/gi, 'token'],
	[/\bdeposit\b/gi, 'get coins'],
	[/\bgamble\b/gi, 'play'],
	[/\bbought\b/gi, 'instantly triggered'],
	[/\bcredit\b/gi, 'coins'],
	[/\bpayouts\b/gi, 'wins'],
	[/\bpayout\b/gi, 'win'],
	[/\bpaying\b/gi, 'winning'],
	[/\bpayer\b/gi, 'winner'],
	[/\brebet\b/gi, 'respin'],
	[/\bwager\b/gi, 'play'],
	// "stake" -> "play amount", mais JAMAIS quand il s'agit de la
	// marque : le disclaimer officiel se termine par "TM et (c) 2026
	// Stake Engine". Le garde (?!\s+engine) protege ce cas.
	[/\bstake\b(?!\s+engine)/gi, 'play amount'],
	[/\bmoney\b/gi, 'coins'],
	[/\bbets\b/gi, 'plays'],
	[/\bbuys\b/gi, 'plays'],
	[/\bcash\b/gi, 'coins'],
	[/\bpaid\b/gi, 'won'],
	[/\bpays\b/gi, 'wins'],
	[/\bbuy\b/gi, 'play'],
	[/\bbet\b/gi, 'play'],
	[/\bpay\b/gi, 'win'],
];

export const estSocial = () => stateUrlDerived.social();

// BET -> PLAY, Bet -> Play, bet -> play. Les libelles du jeu sont en
// majuscules, les phrases des regles non : on suit la casse trouvee.
const respecterLaCasse = (trouve: string, remplacement: string) => {
	if (trouve === trouve.toUpperCase()) return remplacement.toUpperCase();
	if (trouve[0] === trouve[0].toUpperCase())
		return remplacement[0].toUpperCase() + remplacement.slice(1);
	return remplacement;
};

const appliquer = (texte: string) =>
	TABLE.reduce(
		(acc, [motif, mot]) => acc.replace(motif, (trouve) => respecterLaCasse(trouve, mot)),
		texte,
	);

/** Un libelle ou une phrase sans balises. */
export const motSocial = (texte: string) => (estSocial() ? appliquer(texte) : texte);

/**
 * Un fragment HTML. Seul le texte entre > et < est transforme : ni les
 * attributs (src, alt, class), ni le contenu des balises <style>, ou
 * une classe comme .louvo-paytable-grid n'a rien a voir avec un pari.
 */
export const texteSocial = (html: string) => {
	if (!estSocial()) return html;
	return html
		.split(/(<style[\s\S]*?<\/style>)/i)
		.map((morceau) =>
			/^<style/i.test(morceau)
				? morceau
				: morceau.replace(/>([^<]+)</g, (_, t) => '>' + appliquer(t) + '<'),
		)
		.join('');
};
