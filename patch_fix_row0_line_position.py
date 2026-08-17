path = "apps/louvo/src/components/WinLineReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old = "y: getSymbolY(p.row - 1) - 18,"
new = "y: getSymbolY(Math.max(0, p.row - 1)) - 18,"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : index bloque a un minimum de 0, evite l'index -1 invalide pour la rangee du haut.")
