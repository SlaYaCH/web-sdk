path = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const PANEL_X_FRACS = [0.2285, 0.4306, 0.6292];"
new = "const PANEL_X_FRACS = [0.2152, 0.4094, 0.5965];"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : positions horizontales corrigees avec les vraies mesures du rendu.")
