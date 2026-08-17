path = "apps/louvo/src/components/AfterDarkHeartTally.svelte"
with open(path, "r") as f:
    content = f.read()

replacements = [
    ("const HEART_SIZE_FRAC = 0.54725;", "const HEART_SIZE_FRAC = 0.10890;"),
    ("{ downUnits: 27, rightUnits: 27 }, // haut", "{ downUnits: 13.5, rightUnits: 13.5 }, // haut"),
    ("{ downUnits: 27, rightUnits: 9 }, // haut-gauche", "{ downUnits: 13.5, rightUnits: 4.5 }, // haut-gauche"),
    ("{ downUnits: 27, rightUnits: 36 }, // haut-droite", "{ downUnits: 13.5, rightUnits: 18 }, // haut-droite"),
    ("{ downUnits: 27, rightUnits: 9 }, // bas-gauche", "{ downUnits: 13.5, rightUnits: 4.5 }, // bas-gauche"),
    ("{ downUnits: 27, rightUnits: 36 }, // bas-droite", "{ downUnits: 13.5, rightUnits: 18 }, // bas-droite"),
    ("{ downUnits: 27, rightUnits: 27 }, // bas", "{ downUnits: 13.5, rightUnits: 13.5 }, // bas"),
]

missing = []
for old, new in replacements:
    if content.count(old) != 1:
        missing.append(old)
    else:
        content = content.replace(old, new, 1)

if missing:
    print("ERREUR : ancre(s) introuvable(s) - le fichier n'est peut-etre pas dans l'etat attendu :")
    for m in missing:
        print(" -", m)
else:
    with open(path, "w") as f:
        f.write(content)
    print("OK : taille corrigee (base x0.5 au lieu de x2.5) + decalages divises par deux.")
