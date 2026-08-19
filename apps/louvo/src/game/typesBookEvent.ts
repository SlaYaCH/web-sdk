import type { BetType } from 'rgs-requests';
import type { SymbolName, RawSymbol, GameType, Position } from './types';
// book events shared with scatter game
type BookEventReveal = {
	index: number;
	type: 'reveal';
	board: RawSymbol[][];
	paddingPositions: number[];
	anticipation: number[];
	gameType: GameType;
};
type BookEventSetTotalWin = {
	index: number;
	type: 'setTotalWin';
	amount: number;
};
type BookEventFinalWin = {
	index: number;
	type: 'finalWin';
	amount: number;
};
type BookEventFreeSpinTrigger = {
	index: number;
	type: 'freeSpinTrigger';
	totalFs: number;
	positions: Position[];
	tier?: 'speed_dating' | 'after_dark';
};
type BookEventUpdateFreeSpin = {
	index: number;
	type: 'updateFreeSpin';
	amount: number;
	total: number;
};
type BookEventSetWin = {
	index: number;
	type: 'setWin';
	amount: number;
	winLevel: number;
};
type BookEventFreeSpinEnd = {
	index: number;
	type: 'freeSpinEnd';
	amount: number;
	winLevel: number;
};
type BookEventWinInfo = {
	index: number;
	type: 'winInfo';
	totalWin: number;
	wins: {
		symbol: SymbolName;
		kind: number;
		win: number;
		positions: Position[];
		meta: {
			lineIndex: number;
			multiplier: number;
			winWithoutMult: number;
			globalMult: number;
			lineMultiplier: number;
		};
	}[];
};
// customised
type BookEventCreateBonusSnapshot = {
	index: number;
	type: 'createBonusSnapshot';
	bookEvents: BookEvent[];
};
type BookEventMatchDuelReveal = {
	index: number;
	type: 'matchDuelReveal';
	reelIndex: number;
	multiplier: number;
	duelValues: [number, number];
};
type BookEventSuperlikeReveal = {
	index: number;
	type: 'superlikeReveal';
	reelIndex: number;
	multiplier: number;
	likes: number;
	streakTier: number;
	streakHearts: number;
	likePositions: { reelIndex: number; rowIndex: number }[];
};
export type BookEvent =
	| BookEventReveal
	| BookEventWinInfo
	| BookEventSetTotalWin
	| BookEventFreeSpinTrigger
	| BookEventUpdateFreeSpin
	| BookEventCreateBonusSnapshot
	| BookEventFinalWin
	| BookEventSetWin
	| BookEventFreeSpinEnd
	// customised
	| BookEventCreateBonusSnapshot
	| BookEventMatchDuelReveal
	| BookEventSuperlikeReveal;
export type Bet = BetType<BookEvent>;
export type BookEventOfType<T> = Extract<BookEvent, { type: T }>;
export type BookEventContext = { bookEvents: BookEvent[] };
