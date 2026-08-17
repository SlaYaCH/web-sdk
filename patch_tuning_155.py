path = "apps/louvo/src/components/SuperlikeBarilletDisplay.svelte"
with open(path, "r") as f:
    content = f.read()

old_hub = "const HUB_Y = 152;"
new_hub = "const HUB_Y = 155;"

if old_hub not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old_hub, new_hub, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : HUB_Y=155 (taille inchangee a 55px, deja parfaite).")
