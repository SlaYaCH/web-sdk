path = "apps/louvo/src/components/Symbol.svelte"
with open(path, "r") as f:
    content = f.read()

old_derived = """	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 10; // pousse le wild vers le bas de sa case
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));"""
new_derived = """	const isWild = $derived(props.rawSymbol.name === 'W');
	const WILD_Y_OFFSET = 10; // pousse le sprite wild vers le bas de sa case
	const MULTIPLIER_BADGE_Y_OFFSET = 32; // decale le badge nettement plus bas que le sprite, sous le mot WILD
	const adjustedY = $derived((props.y ?? 0) + (isWild ? WILD_Y_OFFSET : 0));
	const badgeY = $derived((props.y ?? 0) + (isWild ? MULTIPLIER_BADGE_Y_OFFSET : 0));"""

old_badge = """	<BitmapText
		anchor={0.5}
		x={props.x}
		y={adjustedY}
		text={`${props.rawSymbol.multiplier}X`}
		zIndex={isExpandingSymbol ? 20 : undefined}
		style={{
			fontFamily: 'gold', fill: 0xff2d6a,
			fontSize: 50,
		}}
	/>"""
new_badge = """	<BitmapText
		anchor={0.5}
		x={props.x}
		y={badgeY}
		text={`${props.rawSymbol.multiplier}X`}
		zIndex={isExpandingSymbol ? 20 : undefined}
		style={{
			fontFamily: 'gold', fill: 0xffffff,
			fontSize: 34,
		}}
	/>"""

missing = [n for n, o in [("derived", old_derived), ("badge", old_badge)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_derived, new_derived, 1)
    content = content.replace(old_badge, new_badge, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : badge multiplicateur repasse en blanc, reduit (34 au lieu de 50), et decale independamment du sprite wild.")
