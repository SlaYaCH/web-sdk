# --- utils.ts : decalage horizontal par colonne, actif seulement en After Dark ---
path = "apps/louvo/src/game/utils.ts"
with open(path, "r") as f:
    content = f.read()

old_import = "import { SYMBOL_WIDTH, REEL_PADDING, SYMBOL_INFO_MAP, BOARD_DIMENSIONS } from './constants';"
new_import = "import { SYMBOL_WIDTH, REEL_PADDING, SYMBOL_INFO_MAP, BOARD_DIMENSIONS, BOARD_SIZES } from './constants';\nimport { stateGame } from './stateGame.svelte';"

old_getx = "export const getSymbolX = (reelIndex: number) => SYMBOL_WIDTH * (reelIndex + REEL_PADDING);"
new_getx = """// Decalages horizontaux specifiques au palier After Dark (le cadre y est
// plus grand) - mesures en jeu par colonne, en % de la largeur totale du
// plateau (BOARD_SIZES.width). Negatif = vers la gauche, positif = vers la
// droite. Un seul tableau a modifier si besoin d'affiner encore.
const AFTER_DARK_COLUMN_ADJUST_FRAC = [-0.04, -0.03, -0.01, 0.02, 0.04];

export const getSymbolX = (reelIndex: number) => {
	const base = SYMBOL_WIDTH * (reelIndex + REEL_PADDING);
	if (stateGame.tier === 'after_dark') {
		return base + AFTER_DARK_COLUMN_ADJUST_FRAC[reelIndex] * BOARD_SIZES.width;
	}
	return base;
};"""

missing = [n for n, o in [("import", old_import), ("getx", old_getx)] if o not in content]
if missing:
    print("ERREUR utils.ts : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_getx, new_getx, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : utils.ts decale chaque colonne selon le palier After Dark.")

# --- stateGame.svelte.ts : descend tout le bloc en After Dark ---
path = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old_layout = """const boardLayout = () => ({
	x: stateLayoutDerived.mainLayout().width * ((GRID_LEFT_FRAC + GRID_RIGHT_FRAC) / 2),
	y: stateLayoutDerived.mainLayout().height * ((GRID_TOP_FRAC + GRID_BOTTOM_FRAC) / 2),
	anchor: { x: 0.5, y: 0.5 },
	pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
	...BOARD_SIZES,
});"""

new_layout = """// 0,5% - descend tout le bloc en After Dark (cadre plus grand que la base)
const AFTER_DARK_Y_ADJUST_FRAC = 0.005;

const boardLayout = () => {
	const afterDarkYAdjust = stateGame.tier === 'after_dark' ? AFTER_DARK_Y_ADJUST_FRAC : 0;
	return {
		x: stateLayoutDerived.mainLayout().width * ((GRID_LEFT_FRAC + GRID_RIGHT_FRAC) / 2),
		y:
			stateLayoutDerived.mainLayout().height *
			((GRID_TOP_FRAC + GRID_BOTTOM_FRAC) / 2 + afterDarkYAdjust),
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
		...BOARD_SIZES,
	};
};"""

if old_layout not in content:
    print("ERREUR stateGame.svelte.ts : ancre introuvable.")
else:
    content = content.replace(old_layout, new_layout, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : stateGame.svelte.ts descend le bloc entier de 0.5% en After Dark.")
