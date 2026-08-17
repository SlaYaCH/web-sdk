# --- Barre de chargement : -2.5% (plus bas) ---
path1 = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path1, "r") as f:
    c1 = f.read()
old1 = "y={context.stateLayoutDerived.mainLayout().height * 0.7252}"
new1 = "y={context.stateLayoutDerived.mainLayout().height * 0.7502}"
if old1 not in c1:
    print("ERREUR LoadingScreen.svelte : ancre introuvable.")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    print("OK : barre descendue de 2.5%.")

# --- Panneau 3 : +5% (plus a droite) ---
path2 = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path2, "r") as f:
    c2 = f.read()
old2 = "const PANEL_X_FRACS = [0.265, 0.4993, 0.6796];"
new2 = "const PANEL_X_FRACS = [0.265, 0.4993, 0.7296];"
if old2 not in c2:
    print("ERREUR LouvoIntroScreen.svelte : ancre introuvable.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    print("OK : MAXIMUM WIN et sa description decales de 5% vers la droite.")
