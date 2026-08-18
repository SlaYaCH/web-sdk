path = "apps/louvo/src/components/WinLineReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const points = props.positions.map((p) => {
		const rawIndex = p.row - 1;
		// Pour la rangee du haut (row=0), rawIndex vaut -1 : on extrapole sa
		// position en reculant d'un ecart de rangee depuis l'indice 0, au
		// lieu de bloquer sur l'indice 0 (ce qui la confondait avec la
		// rangee suivante).
		const rowGap = getSymbolY(1) - getSymbolY(0);
		const y = rawIndex >= 0 ? getSymbolY(rawIndex) - 18 : getSymbolY(0) - rowGap - 18;
		return {
			x: getSymbolX(p.reel),
			y,
		};
	});"""

new = """	const points = props.positions.map((p) => {
		// Confirme en jeu reel (Stake Engine) : chaque ligne s'affichait
		// systematiquement une case en dessous de sa vraie position, sur
		// TOUTES les rangees (pas juste la rangee du haut) - decalage d'un
		// cran de plus par rapport a la version precedente.
		const rawIndex = p.row - 2;
		const rowGap = getSymbolY(1) - getSymbolY(0);
		const y = rawIndex >= 0 ? getSymbolY(rawIndex) - 18 : getSymbolY(0) + rawIndex * rowGap - 18;
		return {
			x: getSymbolX(p.reel),
			y,
		};
	});"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : toutes les lignes remontees d'une case supplementaire (row - 2 au lieu de row - 1).")
