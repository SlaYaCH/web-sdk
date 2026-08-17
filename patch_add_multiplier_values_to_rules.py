path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = """<p><strong>MATCH</strong> triggers a duel between two multiplier values, deciding the multiplier applied to the win.</p>
	<p><strong>SUPER LIKE</strong> sends out extra Wilds carrying its own multiplier.</p>"""

new = """<p><strong>MATCH</strong> triggers a duel between two multiplier values, deciding the multiplier applied to the win.</p>
	<p><strong>SUPER LIKE</strong> sends out extra Wilds carrying its own multiplier.</p>
	<p>Possible multiplier values for MATCH and SUPER LIKE are: 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 200x.</p>"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : liste des 16 valeurs de multiplicateur ajoutee aux vraies regles du jeu.")
