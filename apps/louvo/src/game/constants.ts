import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 120;
export const SYMBOL_WIDTH = 116;
export const SYMBOL_HEIGHT = 91;

export const REEL_PADDING = 0.53;

// initial board (padded top and bottom) - 5 colonnes x 7 lignes
// (5 visibles + 2 de remplissage, pour matcher numRows: [5,5,5,5,5])
export const INITIAL_BOARD: RawSymbol[][] = [
	[{ name: 'L2' }, { name: 'H1' }, { name: 'L4' }, { name: 'H3' }, { name: 'L1' }, { name: 'H5' }, { name: 'L3' }],
	[{ name: 'H2' }, { name: 'L3' }, { name: 'H4' }, { name: 'L1' }, { name: 'H6' }, { name: 'L2' }, { name: 'H1' }],
	[{ name: 'L4' }, { name: 'H5' }, { name: 'L2' }, { name: 'H3' }, { name: 'L3' }, { name: 'H2' }, { name: 'L1' }],
	[{ name: 'H6' }, { name: 'L1' }, { name: 'H4' }, { name: 'L4' }, { name: 'H1' }, { name: 'L2' }, { name: 'H5' }],
	[{ name: 'L3' }, { name: 'H2' }, { name: 'L1' }, { name: 'H6' }, { name: 'L4' }, { name: 'H3' }, { name: 'L2' }],
];

export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: INITIAL_BOARD[0].length - 2 };

export const BOARD_SIZES = {
	width: SYMBOL_WIDTH * BOARD_DIMENSIONS.x,
	height: SYMBOL_HEIGHT * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
const PORTRAIT_HEIGHT = 1422;
export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

// Louvo a 6 portraits (H1-H6), pas 5 comme lines
export const HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const SPIN_OPTIONS_SHARED = {
	reelBounceBackSpeed: 0.15,
	reelSpinSpeedBeforeBounce: 4,
	reelPaddingMultiplierNormal: 1.2,
	reelPaddingMultiplierAnticipated: 10,
	reelSpinDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 2,
	reelSpinSpeed: 3,
	reelBounceSizeMulti: 0.3,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 5,
	reelSpinSpeed: 5,
	reelBounceSizeMulti: 0.05,
};

export const SPIN_OPTIONS_SUPERFAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 9,
	reelSpinSpeed: 9,
	reelBounceSizeMulti: 0.02,
};

export const MOTION_BLUR_VELOCITY = 31;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};

// --- Ratios de taille ---
const portraitSizeRatios = { width: 1, height: 1 };
const baseSymbolSizeRatios = { width: 1, height: 1 };
// WILD / MATCH / DATE : images 1536x1024 (paysage, ratio 1.5:1)
const wideSizeRatios = { width: 1.5, height: 1 };
// Wild specifiquement 10% plus petit que M/S (qui partagent wideSizeRatios) -
// evite que le haut du symbole deborde de sa case.
const wildSizeRatios = { width: 1.5 * 0.9, height: 1 * 0.9 };
// SUPER LIKE : image 1024x1536 (portrait, ratio 1:1.5)
const tallSizeRatios = { width: 1 / 1.5, height: 1 };

const h1Static = { type: 'sprite', assetKey: 'H1', sizeRatios: portraitSizeRatios };
const h2Static = { type: 'sprite', assetKey: 'H2', sizeRatios: portraitSizeRatios };
const h3Static = { type: 'sprite', assetKey: 'H3', sizeRatios: portraitSizeRatios };
const h4Static = { type: 'sprite', assetKey: 'H4', sizeRatios: portraitSizeRatios };
const h5Static = { type: 'sprite', assetKey: 'H5', sizeRatios: portraitSizeRatios };
const h6Static = { type: 'sprite', assetKey: 'H6', sizeRatios: portraitSizeRatios };

const l1Static = { type: 'sprite', assetKey: 'L1', sizeRatios: baseSymbolSizeRatios };
const l2Static = { type: 'sprite', assetKey: 'L2', sizeRatios: baseSymbolSizeRatios };
const l3Static = { type: 'sprite', assetKey: 'L3', sizeRatios: baseSymbolSizeRatios };
const l4Static = { type: 'sprite', assetKey: 'L4', sizeRatios: baseSymbolSizeRatios };

const wStatic = { type: 'sprite', assetKey: 'W', sizeRatios: wildSizeRatios };
const mStatic = { type: 'sprite', assetKey: 'M', sizeRatios: wideSizeRatios };
const sStatic = { type: 'sprite', assetKey: 'S', sizeRatios: wideSizeRatios };
const kStatic = { type: 'sprite', assetKey: 'K', sizeRatios: tallSizeRatios };

// Premier jet : chaque état renvoie vers le même sprite statique, y compris
// `win`. À terme, `win` gagnerait à avoir un traitement distinct (léger
// spritesheet ou tween scale/glow) - cf. discussion sur le niveau
// d'animation à prévoir.
export const SYMBOL_INFO_MAP = {
	H1: { static: h1Static, spin: h1Static, land: h1Static, postWinStatic: h1Static, win: h1Static },
	H2: { static: h2Static, spin: h2Static, land: h2Static, postWinStatic: h2Static, win: h2Static },
	H3: { static: h3Static, spin: h3Static, land: h3Static, postWinStatic: h3Static, win: h3Static },
	H4: { static: h4Static, spin: h4Static, land: h4Static, postWinStatic: h4Static, win: h4Static },
	H5: { static: h5Static, spin: h5Static, land: h5Static, postWinStatic: h5Static, win: h5Static },
	H6: { static: h6Static, spin: h6Static, land: h6Static, postWinStatic: h6Static, win: h6Static },

	L1: { static: l1Static, spin: l1Static, land: l1Static, postWinStatic: l1Static, win: l1Static },
	L2: { static: l2Static, spin: l2Static, land: l2Static, postWinStatic: l2Static, win: l2Static },
	L3: { static: l3Static, spin: l3Static, land: l3Static, postWinStatic: l3Static, win: l3Static },
	L4: { static: l4Static, spin: l4Static, land: l4Static, postWinStatic: l4Static, win: l4Static },

	W: { static: wStatic, spin: wStatic, land: wStatic, postWinStatic: wStatic, win: wStatic },
	M: { static: mStatic, spin: mStatic, land: mStatic, postWinStatic: mStatic, win: mStatic },
	K: { static: kStatic, spin: kStatic, land: kStatic, postWinStatic: kStatic, win: kStatic },
	S: { static: sStatic, spin: sStatic, land: sStatic, postWinStatic: sStatic, win: sStatic },
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;

// Coordonnees mesurees precisement de la grille dans l'image de fond source
// (1672x941) - c'est LA source de verite pour positionner les symboles,
// pas une taille de symbole arbitraire.
const GRID_SOURCE_WIDTH = 1672;
const GRID_SOURCE_HEIGHT = 941;
export const GRID_LEFT_FRAC = 491 / GRID_SOURCE_WIDTH;
export const GRID_RIGHT_FRAC = 1166 / GRID_SOURCE_WIDTH;
export const GRID_TOP_FRAC = 130 / GRID_SOURCE_HEIGHT;
export const GRID_BOTTOM_FRAC = 657 / GRID_SOURCE_HEIGHT;
