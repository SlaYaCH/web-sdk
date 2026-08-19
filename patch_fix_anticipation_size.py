path = "apps/louvo/src/components/Anticipation.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	width={SYMBOL_SIZE * 0.56}
	height={SYMBOL_SIZE * 1.6}"""
new = """	width={SYMBOL_SIZE * 1.0}
	height={SYMBOL_SIZE * 5}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : cadre d'anticipation maintenant taille pleine colonne (largeur 1 symbole, hauteur 5 rangees).")
