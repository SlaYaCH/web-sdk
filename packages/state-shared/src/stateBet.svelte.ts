import type { BaseBet } from 'utils-bet';
import { stateMeta } from './stateMeta.svelte';
import { stateConfig } from './stateConfig.svelte';

export type Currency = string;
export type BetToResume = BaseBet | null;
export type BetModeKey = string;

export const stateBet = $state({
	currency: 'USD' as Currency,
	balanceAmount: 0,
	betAmount: 1,
	wageredBetAmount: 1,
	betToResume: null as BetToResume,
	activeBetModeKey: 'BASE' as BetModeKey,
	winBookEventAmount: 0,
	autoSpinsLoss: 0,
	autoSpinsCounter: 0,
	autoSpinsLossLimitAmount: Infinity,
	autoSpinsSingleWinLimitAmount: Infinity,
	isSpaceHold: false,
	isTurbo: false,
	isSuperTurbo: false,
	stopOnWin: false,
});

// ------------------------------------------------------------------
// ON NE POSE JAMAIS UNE MISE QUI N'EST PAS UN PALIER.     (lot 155)
//
// L'ancienne version rendait `max`, c'est-a-dire le SOLDE EXACT,
// des que la valeur demandee le depassait. Avec 366,60 $ de solde,
// la mise devenait 366,60 $.
//
// Or les paliers viennent de la plateforme (betLevels, renvoye a
// l'authentification). 366,60 n'en est pas un. Au tour suivant le
// RGS repondait 400 Bad Request, en texte brut - et le jeu, qui
// attendait du JSON, s'arretait sur "Sorry, something went wrong".
//
// Reproductible par n'importe qui : monter la mise au maximum,
// appuyer sur SPIN.
//
// On redescend donc au palier autorise le plus proche EN DESSOUS.
// Et si aucun n'est abordable, on pose le plus petit : le montant
// reste valide, et c'est isBetCostAvailable() qui empeche de
// jouer - c'est son role, pas celui d'ici.
//
// Ce point de passage est unique : la barre du bas, le selecteur du
// menu bonus, le menu de mise et les raccourcis clavier passent
// tous par lui.
// ------------------------------------------------------------------
const palierSousLeSolde = (max: number) => {
	const paliers = [...(stateConfig.betAmountOptions ?? [])]
		.filter((palier) => typeof palier === 'number' && palier > 0)
		.sort((a, b) => a - b);
	// Pas de paliers connus (avant l'authentification) : on garde
	// l'ancien comportement plutot que de rendre zero.
	if (paliers.length === 0) return max;
	const abordables = paliers.filter((palier) => palier <= max);
	return abordables.length ? abordables[abordables.length - 1] : paliers[0];
};

const correctBetAmount = (value: number) => {
	if (value <= 0) return 0;
	const costMultiplier = betCostMultiplier();
	if (costMultiplier === 0) return 0;
	const max = stateBet.balanceAmount / costMultiplier;
	if (value < max) return value;
	return palierSousLeSolde(max);
};

const setBetAmount = (value: number) => {
	stateBet.betAmount = correctBetAmount(value);
};

const updateBetAmount = (update: (value: number) => number) => {
	stateBet.betAmount = correctBetAmount(update(stateBet.betAmount));
};

let isTurboLocked = false;

const updateIsTurbo = (value: boolean, options: { persistent: boolean }) => {
	const { persistent } = options;

	if (!persistent && isTurboLocked) return;
	if (persistent) isTurboLocked = value;

	stateBet.isTurbo = value;
};

const activeBetMode = () => stateMeta.betModeMeta?.[stateBet.activeBetModeKey.toUpperCase()]
	?? stateMeta.betModeMeta?.[stateBet.activeBetModeKey.toLowerCase()]
	?? null;
const isContinuousBet = () => stateBet.autoSpinsCounter > 1 || stateBet.isSpaceHold;
const timeScale = () => (stateBet.isSuperTurbo ? 4 : stateBet.isTurbo ? 2 : 1);
const betCostMultiplier = () =>
	stateBetDerived.activeBetMode().type === 'activate'
		? stateBetDerived.activeBetMode().costMultiplier
		: 1;
const betCost = () => stateBet.betAmount * betCostMultiplier();
const isBetCostAvailable = () => betCost() > 0 && betCost() <= stateBet.balanceAmount;
const hasAutoBetCounter = () => stateBet.autoSpinsCounter !== 0;

export const stateBetDerived = {
	setBetAmount,
	updateBetAmount,
	updateIsTurbo,
	activeBetMode,
	isContinuousBet,
	timeScale,
	betCost,
	isBetCostAvailable,
	hasAutoBetCounter,
};
