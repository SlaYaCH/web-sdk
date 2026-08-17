# --- Barre de chargement : calibrage direct cadre-cible vs rendu reel ---
path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old = """            <LoadingProgress
                x={context.stateLayoutDerived.mainLayout().width * 0.4426}
                y={context.stateLayoutDerived.mainLayout().height * 0.6462}
                width={context.stateLayoutDerived.mainLayout().width * 0.317}
                height={context.stateLayoutDerived.mainLayout().height * 0.05}
            >"""
new = """            <LoadingProgress
                x={context.stateLayoutDerived.mainLayout().width * 0.5133}
                y={context.stateLayoutDerived.mainLayout().height * 0.6238}
                width={context.stateLayoutDerived.mainLayout().width * 0.3507}
                height={context.stateLayoutDerived.mainLayout().height * 0.0764}
            >"""

if old not in content:
    print("ERREUR LoadingScreen.svelte : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : barre calibree sur la comparaison directe cadre/rendu.")
