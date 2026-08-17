path = "apps/louvo/src/components/WinLineReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old = "y: getSymbolY(p.row),"
count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    new = "y: getSymbolY(p.row - 1) - 18,"
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : decalage complet applique (1 rangee + 18px, ~1.2 rangee au total vers le haut).")
