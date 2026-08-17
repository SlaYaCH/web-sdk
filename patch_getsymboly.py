path = "apps/louvo/src/game/utils.ts"
with open(path, "r") as f:
    content = f.read()

old_line = "export const getSymbolY = (symbolIndexOfBoard: number) => (symbolIndexOfBoard + 0.5) * SYMBOL_HEIGHT;"

new_block = """// Centres exacts de chaque rangee, mesures precisement dans l'image de
// fond source (1672x941), convertis en fractions.
const ROW_CENTERS_FRAC = [
	(130 + 233) / 2 / 941,
	(237 + 340) / 2 / 941,
	(343 + 446) / 2 / 941,
	(450 + 554) / 2 / 941,
	(557 + 657) / 2 / 941,
];

export const getSymbolY = (symbolIndexOfBoard: number) =>
	stateLayoutDerived.mainLayout().height * ROW_CENTERS_FRAC[symbolIndexOfBoard];"""

if old_line not in content:
    print("ERREUR : ligne getSymbolY non trouvee telle quelle, rien modifie.")
    print("Ligne recherchee :", repr(old_line))
else:
    content = content.replace(old_line, new_block)
    with open(path, "w") as f:
        f.write(content)
    print("OK : getSymbolY remplace.")
