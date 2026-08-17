path = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old_block = """const boardLayout = () => ({
\tx: stateLayoutDerived.mainLayout().width * 0.5,
\ty: stateLayoutDerived.mainLayout().height * 0.5,
\tanchor: { x: 0.5, y: 0.5 },
\tpivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
\t...BOARD_SIZES,
});"""

new_block = """const boardLayout = () => ({
\tx: stateLayoutDerived.mainLayout().width * ((GRID_LEFT_FRAC + GRID_RIGHT_FRAC) / 2),
\ty: stateLayoutDerived.mainLayout().height * ((GRID_TOP_FRAC + GRID_BOTTOM_FRAC) / 2),
\tanchor: { x: 0.5, y: 0.5 },
\tpivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
\t...BOARD_SIZES,
});"""

if old_block not in content:
    print("ERREUR : bloc non trouve tel quel, rien modifie.")
else:
    content = content.replace(old_block, new_block)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bloc deplace vers le centre reel de la grille.")
