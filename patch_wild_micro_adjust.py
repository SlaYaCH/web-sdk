path = "apps/louvo/src/components/Symbol.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 10; // pousse le sprite wild vers le bas de sa case
	const MULTIPLIER_BADGE_Y_OFFSET = 32; // decale le badge nettement plus bas que le sprite, sous le mot WILD
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));
	const badgeY = $derived((props.y ?? 0) + (isWild ? MULTIPLIER_BADGE_Y_OFFSET : 0));"""
new = """	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 5; // pousse le sprite wild vers le bas de sa case (remonte de ~2mm)
	const WILD_X_OFFSET = -3; // decale le sprite wild vers la gauche (~1mm)
	const MULTIPLIER_BADGE_Y_OFFSET = 27; // decale le badge sous le mot WILD (remonte de ~2mm)
	const adjustedX = $derived((props.x ?? 0) + (isWild ? WILD_X_OFFSET : 0));
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));
	const badgeY = $derived((props.y ?? 0) + (isWild ? MULTIPLIER_BADGE_Y_OFFSET : 0));"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    content = content.replace(
        '<SymbolSprite\n\t\t{symbolInfo}\n\t\tx={props.x}\n\t\ty={adjustedY}',
        '<SymbolSprite\n\t\t{symbolInfo}\n\t\tx={adjustedX}\n\t\ty={adjustedY}',
        1,
    )
    with open(path, "w") as f:
        f.write(content)
    print("OK : wild remonte + decale a gauche, badge x7 remonte, independamment l'un de l'autre.")
