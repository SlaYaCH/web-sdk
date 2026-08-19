path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = """	const targets = (props.positions ?? []).map((p) => ({
		x: getSymbolX(p.reelIndex),
		y: getRowY(p.rowIndex),
	}));"""
new1 = """	// Securite : exclut toute position ciblee sur la colonne ou se trouve
	// la banniere elle-meme (ne devrait jamais arriver cote Math SDK, mais
	// un coeur ne doit JAMAIS atterrir sur l'emplacement de la banniere).
	const positions = (props.positions ?? []).filter((p) => p.reelIndex !== props.reelIndex);
	const targets = positions.map((p) => ({
		x: getSymbolX(p.reelIndex),
		y: getRowY(p.rowIndex),
	}));"""
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (targets) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (targets filtres)")

old2 = "const pos = props.positions?.[index];"
new2 = "const pos = positions[index];"
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (pos) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (pos utilise le tableau filtre)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
