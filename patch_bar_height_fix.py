path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const BAR_WIDTH = 1300;
	const BAR_HEIGHT = 224;
	const ROW_Y = BAR_HEIGHT * 0.365 - BAR_HEIGHT / 2;"""
new = """	const BAR_WIDTH = 1300;
	const BAR_HEIGHT = 240;
	const ROW_Y = BAR_HEIGHT * 0.511 - BAR_HEIGHT / 2;"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : hauteur de la barre corrigee, le cercle spin ne devrait plus etre coupe.")
