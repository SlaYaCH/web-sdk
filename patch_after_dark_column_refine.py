path = "apps/louvo/src/game/utils.ts"
with open(path, "r") as f:
    content = f.read()

old = "const AFTER_DARK_COLUMN_ADJUST_FRAC = [-0.04, -0.03, -0.01, 0.02, 0.04];"
new = "const AFTER_DARK_COLUMN_ADJUST_FRAC = [-0.035, -0.02, -0.005, 0.015, 0.03];"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : decalages par colonne affines.")
