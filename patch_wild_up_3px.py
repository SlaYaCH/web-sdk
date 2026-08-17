path = "apps/louvo/src/components/Symbol.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const WILD_Y_OFFSET = 5; // pousse le sprite wild vers le bas de sa case (remonte de ~2mm)"
new = "const WILD_Y_OFFSET = 2; // pousse le sprite wild vers le bas de sa case (remonte de 3px supplementaires)"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : WILD remonte de 3px de plus (5 -> 2).")
