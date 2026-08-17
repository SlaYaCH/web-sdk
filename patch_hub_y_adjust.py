path = "apps/louvo/src/components/SuperlikeBarilletDisplay.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const HUB_Y = 140;"
new = "const HUB_Y = 151;"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : HUB_Y ajuste a 151 (redescendu de la moitie du % monte).")
