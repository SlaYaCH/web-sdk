path = "apps/louvo/src/game/utils.ts"
with open(path, "r") as f:
    content = f.read()

old_line = "export const getSymbolX = (reelIndex: number) => SYMBOL_WIDTH * (reelIndex + REEL_PADDING);"

new_block = """// Centres exacts de chaque colonne, mesures precisement dans l'image de
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

if old_line not in content:
    print("ERREUR : ligne getSymbolX non trouvee telle quelle, rien modifie.")
    print("Ligne recherchee :", repr(old_line))
else:
    content = content.replace(old_line, new_block)
    import_line = "import { stateLayoutDerived } from './stateLayout';\n"
    if "from './stateLayout'" not in content:
        content = import_line + content
    with open(path, "w") as f:
        f.write(content)
    print("OK : getSymbolX remplace, import ajoute.")
