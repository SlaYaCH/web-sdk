path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const originY = -30; // approximativement la hauteur des mains/buste sur la banniere"
new = "const originY = 162.7; // centre du barillet dessine dans la banniere (mesure sur l'asset natif)"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les coeurs partent maintenant du vrai centre du barillet.")
