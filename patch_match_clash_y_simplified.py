path = "apps/louvo/src/components/MatchDuelClash.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const Y_POSITION = 146; // ~82% de la hauteur de la banniere (vers le bas du cadrage)"
new = "const Y_POSITION = 114; // pile entre le milieu (0) et le bas de la banniere"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Y_POSITION = 114 (exactement entre le milieu et le bas).")
