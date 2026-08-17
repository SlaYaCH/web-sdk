# --- Barre : epaisseur +5% relatif, position inchangee ---
path1 = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path1, "r") as f:
    c1 = f.read()
old1 = "height={context.stateLayoutDerived.mainLayout().height * 0.0499}"
new1 = "height={context.stateLayoutDerived.mainLayout().height * 0.0524}"
if old1 not in c1:
    print("ERREUR LoadingScreen.svelte : ancre introuvable.")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    print("OK : epaisseur de la barre augmentee de 5% (position x/y inchangee).")

# --- Panneau 3 : -1% (encore un peu a gauche) ---
path2 = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path2, "r") as f:
    c2 = f.read()
old2 = "const PANEL_X_FRACS = [0.265, 0.4993, 0.7296];"
new2 = "const PANEL_X_FRACS = [0.265, 0.4993, 0.7196];"
if old2 not in c2:
    print("ERREUR LouvoIntroScreen.svelte : ancre introuvable.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    print("OK : MAXIMUM WIN et sa description decales de 1% vers la gauche.")
