import re

path = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old_block = """const boardLayout = () => ({
	x: stateLayoutDerived.mainLayout().width * 0.5,
	y: stateLayoutDerived.mainLayout().height * 0.5,
	anchor: { x: 0.5, y: 0.5 },
	pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
	...BOARD_SIZES,
});"""

new_block = """const boardLayout = () => {
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

if old_block not in content:
    print("ERREUR : le bloc exact n'a pas ete trouve, rien modifie.")
else:
    content = content.replace(old_block, new_block)
    with open(path, "w") as f:
        f.write(content)
    print("OK : boardLayout() remplace avec succes.")

import_line = "import { GRID_LEFT_FRAC, GRID_RIGHT_FRAC, GRID_TOP_FRAC, GRID_BOTTOM_FRAC } from './constants';\n"
with open(path, "r") as f:
    content = f.read()
if "GRID_LEFT_FRAC" not in content.split("\n")[0]:
    content = import_line + content
    with open(path, "w") as f:
        f.write(content)
    print("OK : import ajoute en haut du fichier.")
else:
    print("Import deja present, rien ajoute.")
