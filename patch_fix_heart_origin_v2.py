path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { getSymbolX, getSymbolY } from '../game/utils';"
new_import = "import { getSymbolX, getSymbolY } from '../game/utils';\n\timport { BOARD_SIZES } from '../game/constants';"

old_origin = """const originX = getSymbolX(props.reelIndex);
	const originY = 162.7; // centre du barillet dessine dans la banniere (mesure sur l'asset natif)"""
new_origin = """const originX = getSymbolX(props.reelIndex);
	// Le barillet est mesure dans le repere LOCAL de BannerReveal (centre = 0,
	// haut du plateau = -BOARD_SIZES.height/2). Ce composant-ci vit dans le
	// repere du PLATEAU entier (0 = haut), pas celui de la banniere - d'ou le
	// decalage de BOARD_SIZES.height/2 pour retomber au bon endroit.
	const originY = BOARD_SIZES.height / 2 + 162.7;"""

if old_import not in content or old_origin not in content:
    print("ERREUR : ancre(s) non trouvee(s).")
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_origin, new_origin, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : origine des coeurs recalee dans le bon repere de coordonnees.")
