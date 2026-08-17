path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = """<p><strong>AFTER DARK</strong> — 150x your bet — instantly unlocks 10 free spins in the nighttime setting.</p>
</div>`}"""

new = """<p><strong>AFTER DARK</strong> — 150x your bet — instantly unlocks 10 free spins in the nighttime setting.</p>

	<h2>BET</h2>
	<p>Bet levels range from 0.10 to 2000 in your selected currency. Bonus buys and other special feature purchases can cost more than the maximum base bet.</p>
</div>`}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : section BET ajoutee aux regles (0.10 a 2000, note sur les achats de fonction speciale).")
