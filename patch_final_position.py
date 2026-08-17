path1 = "apps/louvo/src/game/utils.ts"
with open(path1, "r") as f:
    content1 = f.read()

old_getx = """// Centres exacts de chaque colonne, mesures precisement dans l'image de
// fond source (1672x941), convertis en fractions pour s'adapter a
// n'importe quelle taille d'ecran reelle.
const COLUMN_CENTERS_FRAC = [
	(491 + 624) / 2 / 1672,
	(627 + 759) / 2 / 1672,
	(762 + 895) / 2 / 1672,
	(898 + 1031) / 2 / 1672,
	(1034 + 1166) / 2 / 1672,
];

export const getSymbolX = (reelIndex: number) =>
	stateLayoutDerived.mainLayout().width * COLUMN_CENTERS_FRAC[reelIndex];"""

new_getx = """export const getSymbolX = (reelIndex: number) => {
	const gridWidth =
		stateLayoutDerived.mainLayout().width * (GRID_RIGHT_FRAC - GRID_LEFT_FRAC);
	return (gridWidth / BOARD_DIMENSIONS.x) * (reelIndex + 0.5);
};"""

if old_getx not in content1:
    print("ERREUR etape 1 : bloc getSymbolX non trouve tel quel.")
else:
    content1 = content1.replace(old_getx, new_getx)
    if "GRID_LEFT_FRAC" not in content1.split("export const getSymbolX")[0]:
        content1 = "import { GRID_LEFT_FRAC, GRID_RIGHT_FRAC } from './constants';\n" + content1
    with open(path1, "w") as f:
        f.write(content1)
    print("OK etape 1 : getSymbolX corrige (coordonnee locale).")

path2 = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path2, "r") as f:
    content2 = f.read()

old_boardlayout = """const boardLayout = () => {
	const mainWidth = stateLayoutDerived.mainLayout().width;
	const mainHeight = stateLayoutDerived.mainLayout().height;
	const gridWidth = mainWidth * (GRID_RIGHT_FRAC - GRID_LEFT_FRAC);
	const gridHeight = mainHeight * (GRID_BOTTOM_FRAC - GRID_TOP_FRAC);
	return {
		x: mainWidth * GRID_LEFT_FRAC + gridWidth / 2,
		y: mainHeight * GRID_TOP_FRAC + gridHeight / 2,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
		width: gridWidth,
		height: gridHeight,
	};
};"""

new_boardlayout = """const boardLayout = () => {
	const mainWidth = stateLayoutDerived.mainLayout().width;
	const mainHeight = stateLayoutDerived.mainLayout().height;
	const gridWidth = mainWidth * (GRID_RIGHT_FRAC - GRID_LEFT_FRAC);
	const gridHeight = mainHeight * (GRID_BOTTOM_FRAC - GRID_TOP_FRAC);
	return {
		x: mainWidth * GRID_LEFT_FRAC + gridWidth / 2,
		y: mainHeight * GRID_TOP_FRAC + gridHeight / 2,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: gridWidth / 2, y: gridHeight / 2 },
	};
};"""

if old_boardlayout not in content2:
    print("ERREUR etape 2 : bloc boardLayout non trouve tel quel.")
else:
    content2 = content2.replace(old_boardlayout, new_boardlayout)
    with open(path2, "w") as f:
        f.write(content2)
    print("OK etape 2 : boardLayout corrige (pivot coherent avec la grille mesuree).")
