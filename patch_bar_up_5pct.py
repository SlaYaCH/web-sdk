path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old = "y={context.stateLayoutDerived.mainLayout().height * 0.7752}"
new = "y={context.stateLayoutDerived.mainLayout().height * 0.7252}"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : barre remontee de 5%.")
