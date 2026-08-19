path = "apps/louvo/src/components/FreeSpinIntro.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	<Sprite
		anchor={0.5}
		x={context.stateLayoutDerived.canvasSizes().width / 2}
		y={context.stateLayoutDerived.canvasSizes().height / 2}
		width={context.stateLayoutDerived.canvasSizes().width}
		height={context.stateLayoutDerived.canvasSizes().height}
		key={context.stateGame.tier === 'after_dark' ? 'afterDarkAnnounce' : 'speedDatingAnnounce'}
	/>"""
new = """	<Sprite
		anchor={0.5}
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height * 0.5}
		width={context.stateLayoutDerived.mainLayout().width}
		height={context.stateLayoutDerived.mainLayout().height}
		key={context.stateGame.tier === 'after_dark' ? 'afterDarkAnnounce' : 'speedDatingAnnounce'}
	/>"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : utilise maintenant mainLayout(), exactement comme boardBackground.")
