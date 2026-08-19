path = "apps/louvo/src/components/FreeSpinIntro.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "import { CanvasSizeRectangle } from 'components-layout';"
new1 = "import { CanvasSizeRectangle, MainContainer } from 'components-layout';"
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (import) : {n} fois - MainContainer peut-etre deja importe ailleurs, verification manuelle necessaire.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (import MainContainer)")

old2 = """	<Sprite
		anchor={0.5}
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height * 0.5}
		width={context.stateLayoutDerived.mainLayout().width}
		height={context.stateLayoutDerived.mainLayout().height}
		key={context.stateGame.tier === 'after_dark' ? 'afterDarkAnnounce' : 'speedDatingAnnounce'}
	/>"""
new2 = """	<MainContainer>
		<Sprite
			anchor={0.5}
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.5}
			width={context.stateLayoutDerived.mainLayout().width}
			height={context.stateLayoutDerived.mainLayout().height}
			key={context.stateGame.tier === 'after_dark' ? 'afterDarkAnnounce' : 'speedDatingAnnounce'}
		/>
	</MainContainer>"""
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (wrap) : {n} fois - verification manuelle necessaire.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (wrap) : Sprite enveloppe dans MainContainer, comme louvoIntroScreen.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
