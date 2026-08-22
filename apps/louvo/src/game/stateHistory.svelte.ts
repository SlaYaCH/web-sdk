import { stateBet } from 'state-shared';
import { API_AMOUNT_MULTIPLIER } from 'constants-shared/bet';

// ------------------------------------------------------------------
// Historique LOCAL de la session courante.
//
// Le RGS de Stake n'expose aucune route d'historique : les 9 routes du
// SDK sont /wallet/authenticate, /wallet/play, /wallet/end-round,
// /wallet/balance, /bet/event, /bet/action, /bet/replay/..., /game/search
// et /session/start. On garde donc nous-memes les tours joues.
//
// A ne PAS confondre avec le Replay officiel Stake, qui recoit un Event ID
// de simulation math dans l'URL. Le betID stocke ici n'est pas un Event ID
// et n'est jamais envoye a /bet/replay.
// ------------------------------------------------------------------
export type HistoryRound = {
	key: number;
	id: string;
	date: string;
	time: string;
	mode: string;
	betAmount: number;
	winAmount: number;
	multiplier: number;
	bet: unknown;
};

const MAX_ROUNDS = 50;
let counter = 0;

export const stateHistory = $state({ rounds: [] as HistoryRound[] });

const deux = (n: number) => String(n).padStart(2, '0');

export const recordRound = (bet: unknown) => {
	// Enregistrer l'historique ne doit JAMAIS pouvoir casser un tour :
	// tout est enferme dans un try/catch.
	try {
		const raw = bet as {
			betID?: number | string;
			roundID?: number | string;
			amount?: number;
			payout?: number;
			payoutMultiplier?: number;
			mode?: string;
		};

		const id = String(raw?.betID ?? raw?.roundID ?? '');

		// Une reprise de partie rejoue le meme round : on ne l'ajoute pas deux fois.
		if (id && stateHistory.rounds[0]?.id === id) return;

		const betAmount =
			typeof raw?.amount === 'number' && raw.amount > 0
				? raw.amount / API_AMOUNT_MULTIPLIER
				: stateBet.wageredBetAmount;
		const payout = typeof raw?.payout === 'number' ? raw.payout / API_AMOUNT_MULTIPLIER : null;
		const multiplier =
			typeof raw?.payoutMultiplier === 'number'
				? raw.payoutMultiplier
				: payout !== null && betAmount > 0
					? payout / betAmount
					: 0;
		const winAmount = payout !== null ? payout : betAmount * multiplier;

		const now = new Date();
		counter += 1;

		stateHistory.rounds.unshift({
			key: counter,
			id: id || '-',
			date: deux(now.getDate()) + '/' + deux(now.getMonth() + 1),
			time: deux(now.getHours()) + ':' + deux(now.getMinutes()) + ':' + deux(now.getSeconds()),
			mode: raw?.mode || stateBet.activeBetModeKey || 'BASE',
			betAmount,
			winAmount,
			multiplier,
			bet,
		});

		if (stateHistory.rounds.length > MAX_ROUNDS) stateHistory.rounds.length = MAX_ROUNDS;
	} catch (error) {
		console.error('history: enregistrement impossible', error);
	}
};
