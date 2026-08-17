import { GRID_LEFT_FRAC, GRID_RIGHT_FRAC } from './constants';
import { stateLayoutDerived } from './stateLayout';
import _ from 'lodash';
import { stateBet } from 'state-shared';
import { createPlayBookUtils } from 'utils-book';
import { createGetEmptyPaddedBoard } from 'utils-slots';

import { SYMBOL_WIDTH, REEL_PADDING, SYMBOL_INFO_MAP, BOARD_DIMENSIONS, BOARD_SIZES } from './constants';
import { stateGame } from './stateGame.svelte';
import { eventEmitter } from './eventEmitter';
import type { Bet, BookEventOfType } from './typesBookEvent';
import { bookEventHandlerMap } from './bookEventHandlerMap';
import type { RawSymbol, SymbolState } from './types';

// general utils
export const { getEmptyBoard } = createGetEmptyPaddedBoard({ reelsDimensions: BOARD_DIMENSIONS });
export const { playBookEvent, playBookEvents } = createPlayBookUtils({ bookEventHandlerMap });
export const playBet = async (bet: Bet) => {
	// Signale qu'un nouveau spin demarre - permet a une UI encore ouverte
	// (ex: banniere de reveal du spin precedent) de se refermer d'elle-meme
	// au lieu de dependre d'un minuteur arbitraire.
	eventEmitter.broadcast({ type: 'spinStart' });
	stateBet.winBookEventAmount = 0;
	await playBookEvents(bet.state);
	eventEmitter.broadcast({ type: 'stopButtonEnable' });
};

// resume bet
const BOOK_EVENT_TYPES_TO_RESERVE_FOR_SNAPSHOT = [
	'updateGlobalMult',
	'freeSpinTrigger',
	'updateFreeSpin',
	'setTotalWin',
];

export const convertTorResumableBet = (betToResume: Bet) => {
	const resumingIndex = Number(betToResume.event);
	const bookEventsBeforeResume = betToResume.state.filter(
		(_, eventIndex) => eventIndex < resumingIndex,
	);
	const bookEventsAfterResume = betToResume.state.filter(
		(_, eventIndex) => eventIndex >= resumingIndex,
	);

	const bookEventToCreateSnapshot: BookEventOfType<'createBonusSnapshot'> = {
		index: 0,
		type: 'createBonusSnapshot',
		bookEvents: bookEventsBeforeResume.filter((bookEvent) =>
			BOOK_EVENT_TYPES_TO_RESERVE_FOR_SNAPSHOT.includes(bookEvent.type),
		),
	};

	const stateToResume = [bookEventToCreateSnapshot, ...bookEventsAfterResume];

	return { ...betToResume, state: stateToResume };
};

// other utils
// Decalages horizontaux specifiques au palier After Dark (le cadre y est
// plus grand) - mesures en jeu par colonne, en % de la largeur totale du
// plateau (BOARD_SIZES.width). Negatif = vers la gauche, positif = vers la
// droite. Un seul tableau a modifier si besoin d'affiner encore.
const AFTER_DARK_COLUMN_ADJUST_FRAC = [-0.035, -0.02, -0.005, 0.015, 0.03];

export const getSymbolX = (reelIndex: number) => {
	const base = SYMBOL_WIDTH * (reelIndex + REEL_PADDING);
	if (stateGame.tier === 'after_dark') {
		return base + AFTER_DARK_COLUMN_ADJUST_FRAC[reelIndex] * BOARD_SIZES.width;
	}
	return base;
};
// Centres exacts de chaque rangee, mesures precisement dans l'image de
// fond source (1672x941), convertis en fractions.
const ROW_CENTERS_FRAC = [
	(130 + 233) / 2 / 941,
	(237 + 340) / 2 / 941,
	(343 + 446) / 2 / 941,
	(450 + 554) / 2 / 941,
	(557 + 657) / 2 / 941,
];

export const getSymbolY = (symbolIndexOfBoard: number) =>
	stateLayoutDerived.mainLayout().height * ROW_CENTERS_FRAC[symbolIndexOfBoard];

export const getSymbolInfo = ({
	rawSymbol,
	state,
}: {
	rawSymbol: RawSymbol;
	state: SymbolState;
}) => {
	return SYMBOL_INFO_MAP[rawSymbol.name][state];
};
