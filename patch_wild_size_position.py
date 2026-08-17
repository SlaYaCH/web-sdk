# --- constants.ts : taille du wild reduite de 10%, sans toucher M/S ---
path = "apps/louvo/src/game/constants.ts"
with open(path, "r") as f:
    content = f.read()

old1 = "const wideSizeRatios = { width: 1.5, height: 1 };"
new1 = """const wideSizeRatios = { width: 1.5, height: 1 };
// Wild specifiquement 10% plus petit que M/S (qui partagent wideSizeRatios) -
// evite que le haut du symbole deborde de sa case.
const wildSizeRatios = { width: 1.5 * 0.9, height: 1 * 0.9 };"""

old2 = "const wStatic = { type: 'sprite', assetKey: 'W', sizeRatios: wideSizeRatios };"
new2 = "const wStatic = { type: 'sprite', assetKey: 'W', sizeRatios: wildSizeRatios };"

missing = [n for n, o in [("1", old1), ("2", old2)] if o not in content]
if missing:
    print("ERREUR constants.ts : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : wild.png rendu 10% plus petit (M et S inchanges).")

# --- Symbol.svelte : pousser le wild vers le bas de sa case ---
path = "apps/louvo/src/components/Symbol.svelte"
with open(path, "r") as f:
    content = f.read()

old3 = "const isExpandingSymbol = $derived(props.rawSymbol.name === 'M' || props.rawSymbol.name === 'K');"
new3 = """const isExpandingSymbol = $derived(props.rawSymbol.name === 'M' || props.rawSymbol.name === 'K');
	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 10; // pousse le wild vers le bas de sa case
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));"""

old4 = """	<SymbolSprite
		{symbolInfo}
		x={props.x}
		y={props.y}
		oncomplete={props.oncomplete}
		zIndex={isExpandingSymbol ? 20 : undefined}
	/>"""
new4 = """	<SymbolSprite
		{symbolInfo}
		x={props.x}
		y={adjustedY}
		oncomplete={props.oncomplete}
		zIndex={isExpandingSymbol ? 20 : undefined}
	/>"""

old5 = """	<BitmapText
		anchor={0.5}
		x={props.x}
		y={props.y}
		text={`${props.rawSymbol.multiplier}X`}"""
new5 = """	<BitmapText
		anchor={0.5}
		x={props.x}
		y={adjustedY}
		text={`${props.rawSymbol.multiplier}X`}"""

missing2 = [n for n, o in [("3", old3), ("4", old4), ("5", old5)] if o not in content]
if missing2:
    print("ERREUR Symbol.svelte : ancre(s) introuvable(s) :", missing2)
else:
    content = content.replace(old3, new3, 1)
    content = content.replace(old4, new4, 1)
    content = content.replace(old5, new5, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : wild (et son badge multiplicateur) decale vers le bas de sa case.")
