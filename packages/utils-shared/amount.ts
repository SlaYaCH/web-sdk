import { stateI18n } from 'state-shared';

import { BOOK_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { stateBet } from 'state-shared';

const NO_LOCALISATION_CURRENCY_MAP: Record<string, string> = {
	XGC: 'GC',
	XSC: 'SC',
};

// bookEventAmount: is the amount or win numbers in the events of books, e.g. the amount in setTotalWin bookEvent
// {
// 	"index": 3,
// 	"type": "setTotalWin",
// 	"amount": 100
// },
// if betting on $1,   100 bookEventAmount equals to $1.    betAmountMultiplier is (100 / BOOK_AMOUNT_MULTIPLIER =) 1
// if betting on $1,    50 bookEventAmount equals to $0.5.  betAmountMultiplier is ( 50 / BOOK_AMOUNT_MULTIPLIER =) 0.5
// if betting on $0.5, 100 bookEventAmount equals to $0.5.  betAmountMultiplier is (100 / BOOK_AMOUNT_MULTIPLIER =) 1
// if betting on $0.5,  50 bookEventAmount equals to $0.25. betAmountMultiplier is ( 50 / BOOK_AMOUNT_MULTIPLIER =) 0.5

export const bookEventAmountToBetAmountMultiplier = (bookEventAmount: number) =>
	bookEventAmount / BOOK_AMOUNT_MULTIPLIER;

export const bookEventAmountToNormalisedAmount = (bookEventAmount: number) => {
	const betAmountMultiplier = bookEventAmountToBetAmountMultiplier(bookEventAmount);
	return stateBet.wageredBetAmount * betAmountMultiplier;
};

export const numberToFloat = (value: number) => Number.parseFloat(`${value}`);

// ============================================================
// LE NOMBRE DE DECIMALES
//
// Cette fonction imposait minimumFractionDigits: 2 et
// maximumFractionDigits: 2 a TOUTES les devises. Deux consequences,
// toutes deux visibles a l'ecran :
//
//   - le yen, seule devise sans decimales du tableau Stake,
//     s'affichait "940,00 JPY" au lieu de "940 JPY" ;
//   - un gain plus petit qu'un centime s'affichait "0.00", alors que
//     le joueur a bien gagne quelque chose.
//
// Intl connait le nombre naturel de decimales de chaque devise : 2
// pour l'euro et le dollar, 0 pour le yen, 3 pour le dinar. On le
// laisse decider, et on n'ajoute des decimales que lorsqu'un montant
// NON NUL s'afficherait autrement comme zero.
// ============================================================

const DECIMALES_MAX = 8;

const decimalesNaturelles = (currency: string) => {
	try {
		return (
			new Intl.NumberFormat('en', { style: 'currency', currency }).resolvedOptions()
				.maximumFractionDigits ?? 2
		);
	} catch {
		// Devise inconnue d'Intl : on retombe sur le comportement d'avant.
		return 2;
	}
};

const decimalesVisibles = (value: number, naturelles: number) => {
	if (!value) return naturelles;
	let decimales = naturelles;
	// Tant que le montant s'arrondirait a zero, on ajoute une decimale.
	while (decimales < DECIMALES_MAX && Math.abs(value) < 0.5 * Math.pow(10, -decimales)) {
		decimales += 1;
	}
	return decimales;
};

export const numberToCurrencyString = (value: number) => {
	if (stateBet.currency in NO_LOCALISATION_CURRENCY_MAP) {
		return `${NO_LOCALISATION_CURRENCY_MAP[stateBet.currency]} ${numberToFloat(value).toFixed(2)}`;
	}

	const naturelles = decimalesNaturelles(stateBet.currency);

	return stateI18n.i18n.number(value, {
		minimumFractionDigits: naturelles,
		maximumFractionDigits: decimalesVisibles(value, naturelles),
		style: 'currency',
		currency: stateBet.currency,
		// numberingSystem: 'latn',
	});
};

export const bookEventAmountToCurrencyString = (bookEventAmount: number) => {
	const normalisedAmount = bookEventAmountToNormalisedAmount(bookEventAmount);
	return numberToCurrencyString(normalisedAmount);
};
