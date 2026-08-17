path = "apps/louvo/src/components/WinLineReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const points = props.positions.map((p) => ({
		x: getSymbolX(p.reel),
		y: getSymbolY(p.row - 1),
	}));"""
new = """	const EXTRA_Y_LIFT = 18; // ~0.2 rangee de plus, en plus du decalage d'une rangee (row - 1)
	const points = props.positions.map((p) => ({
		x: getSymbolX(p.reel),
		y: getSymbolY(p.row - 1) - EXTRA_Y_LIFT,
	}));"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois) - le fichier a peut-etre change, verification manuelle necessaire.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : decalage total d'environ 1.2 rangee vers le haut.")
