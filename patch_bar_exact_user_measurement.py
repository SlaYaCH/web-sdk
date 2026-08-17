path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old = """            <LoadingProgress
                x={context.stateLayoutDerived.mainLayout().width * 0.4623}
                y={context.stateLayoutDerived.mainLayout().height * 0.7641}
                width={context.stateLayoutDerived.mainLayout().width * 0.3316}
                height={context.stateLayoutDerived.mainLayout().height * 0.0468}
            >"""
new = """            <LoadingProgress
                x={context.stateLayoutDerived.mainLayout().width * 0.5009}
                y={context.stateLayoutDerived.mainLayout().height * 0.7752}
                width={context.stateLayoutDerived.mainLayout().width * 0.3343}
                height={context.stateLayoutDerived.mainLayout().height * 0.0499}
            >"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : position exacte mesuree par detection de pixels sur votre fichier.")
