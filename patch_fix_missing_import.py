path = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old = "\tSPIN_OPTIONS_FAST,\n"
count = content.count(old)
if count != 1:
    print(f"ERREUR : '{old.strip()}' trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, old + "\tSPIN_OPTIONS_SUPERFAST,\n", 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SPIN_OPTIONS_SUPERFAST ajoute a l'import.")
