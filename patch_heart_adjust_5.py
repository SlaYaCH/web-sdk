path = "apps/louvo/src/components/AfterDarkHeartTally.svelte"
with open(path, "r") as f:
    content = f.read()

replacements = [
    ("{ downUnits: 8.5, rightUnits: 6.5 }, // haut", "{ downUnits: 9.5, rightUnits: 7.5 }, // haut"),
    ("{ downUnits: 12.5, rightUnits: 12.5 }, // haut-droite", "{ downUnits: 12.5, rightUnits: 13 }, // haut-droite"),
    ("{ downUnits: 12.5, rightUnits: 13 }, // bas-droite", "{ downUnits: 12.5, rightUnits: 14 }, // bas-droite"),
    ("{ downUnits: 21, rightUnits: 8 }, // bas", "{ downUnits: 20.5, rightUnits: 8 }, // bas"),
]

missing = []
for old, new in replacements:
    if content.count(old) != 1:
        missing.append(old)
    else:
        content = content.replace(old, new, 1)

if missing:
    print("ERREUR : ancre(s) introuvable(s) - le fichier n'est plus dans l'etat attendu :")
    for m in missing:
        print(" -", m)
else:
    with open(path, "w") as f:
        f.write(content)
    print("OK : haut, haut-droite, bas-droite ajustes ; bas monte seulement (pas de deplacement lateral cette fois).")
