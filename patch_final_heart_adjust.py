path = "apps/louvo/src/components/AfterDarkHeartTally.svelte"
with open(path, "r") as f:
    content = f.read()

replacements = [
    ("const HEART_SIZE_FRAC = 0.10890;", "const HEART_SIZE_FRAC = 0.49253;"),
    ("{ downUnits: 13.5, rightUnits: 13.5 }, // haut", "{ downUnits: 4.5, rightUnits: 4.5 }, // haut"),
    ("{ downUnits: 13.5, rightUnits: 4.5 }, // haut-gauche", "{ downUnits: 12.5, rightUnits: 3.5 }, // haut-gauche"),
    ("{ downUnits: 13.5, rightUnits: 18 }, // haut-droite", "{ downUnits: 12.5, rightUnits: 9 }, // haut-droite"),
    ("{ downUnits: 13.5, rightUnits: 4.5 }, // bas-gauche", "{ downUnits: 12.5, rightUnits: 3.5 }, // bas-gauche"),
    ("{ downUnits: 13.5, rightUnits: 18 }, // bas-droite", "{ downUnits: 12.5, rightUnits: 9 }, // bas-droite"),
    ("{ downUnits: 13.5, rightUnits: 13.5 }, // bas", "{ downUnits: 22.5, rightUnits: 4.5 }, // bas"),
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
    print()
    print("Contenu actuel du fichier pour verification :")
else:
    with open(path, "w") as f:
        f.write(content)
    print("OK : taille et positions corrigees.")
