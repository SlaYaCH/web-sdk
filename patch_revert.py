import re

path1 = "apps/louvo/src/game/utils.ts"
with open(path1) as f:
    c1 = f.read()
c1 = re.sub(
    r"export const getSymbolX = \(reelIndex: number\) => \{.*?\n\};",
    "export const getSymbolX = (reelIndex: number) => SYMBOL_SIZE * (reelIndex + REEL_PADDING);",
    c1, flags=re.DOTALL
)
with open(path1, "w") as f:
    f.write(c1)

path2 = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path2) as f:
    c2 = f.read()
c2 = re.sub(
    r"const boardLayout = \(\) => \{.*?\n\};",
    "const boardLayout = () => ({\n\tx: stateLayoutDerived.mainLayout().width * 0.5,\n\ty: stateLayoutDerived.mainLayout().height * 0.5,\n\tanchor: { x: 0.5, y: 0.5 },\n\tpivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },\n\t...BOARD_SIZES,\n});",
    c2, flags=re.DOTALL
)
c2 = c2.replace(
    "symbolHeight: stateLayoutDerived.mainLayout().height * (GRID_BOTTOM_FRAC - GRID_TOP_FRAC) / BOARD_DIMENSIONS.y,",
    "symbolHeight: SYMBOL_SIZE,"
)
with open(path2, "w") as f:
    f.write(c2)

print("Tout revenu a l'etat stable d'avant les reglages de position.")
