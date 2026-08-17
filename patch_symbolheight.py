path = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old_line = "\t\tsymbolHeight: SYMBOL_SIZE,"
new_line = "\t\tsymbolHeight: stateLayoutDerived.mainLayout().height * (GRID_BOTTOM_FRAC - GRID_TOP_FRAC) / BOARD_DIMENSIONS.y,"

if old_line not in content:
    print("ERREUR : ligne non trouvee telle quelle.")
    print("Recherchee :", repr(old_line))
else:
    content = content.replace(old_line, new_line)
    with open(path, "w") as f:
        f.write(content)
    print("OK : symbolHeight corrige avec les vraies mesures.")
