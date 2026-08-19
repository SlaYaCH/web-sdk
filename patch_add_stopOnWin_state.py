path = "packages/state-shared/src/stateBet.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old = "\tisTurbo: false,\n\tisSuperTurbo: false,"
new = "\tisTurbo: false,\n\tisSuperTurbo: false,\n\tstopOnWin: false,"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : stopOnWin ajoute a stateBet (false par defaut, comme demande).")
