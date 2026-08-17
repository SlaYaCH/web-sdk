path = "apps/louvo/src/components/AfterDarkHeartTally.svelte"
with open(path, "r") as f:
    content = f.read()

replacements = [
    ("const HEART_SIZE_FRAC = 0.49253;", "const HEART_SIZE_FRAC = 0.44328;"),
    ("{ downUnits: 4.5, rightUnits: 4.5 }, // haut", "{ downUnits: 6.5, rightUnits: 2.5 }, // haut"),
    ("{ downUnits: 12.5, rightUnits: 9 }, // haut-droite", "{ downUnits: 12.5, rightUnits: 11 }, // haut-droite"),
    ("{ downUnits: 12.5, rightUnits: 9 }, // bas-droite", "{ downUnits: 12.5, rightUnits: 11 }, // bas-droite"),
    ("{ downUnits: 22.5, rightUnits: 4.5 }, // bas", "{ downUnits: 22.5, rightUnits: 6.5 }, // bas"),
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
    print("OK : taille reduite de 10%, positions haut/haut-droite/bas-droite/bas ajustees (gauche/haut-gauche inchanges).")
