path = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const PANEL_X_FRACS = [0.265, 0.4993, 0.7146];"
new = "const PANEL_X_FRACS = [0.265, 0.4993, 0.6646];"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : MAXIMUM WIN et sa description decales de 5% vers la gauche.")
