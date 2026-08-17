path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const BONUS_X = -BAR_WIDTH / 2 - 90;"
new = "const BONUS_X = -BAR_WIDTH / 2 - 45; // rapproche pour rester dans le cadre visible"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bouton bonus rapproche de la barre.")
