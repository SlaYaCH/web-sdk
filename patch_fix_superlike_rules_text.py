path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "<p>The SUPER LIKE symbol sends out between 1 and 6 Wilds to random empty positions on the grid, each carrying the same multiplier drawn for the Super Like itself.</p>"
new1 = "<p>The SUPER LIKE symbol sends out between 1 and 6 Wilds to random empty positions on the grid.</p>"
count1 = content.count(old1)
if count1 != 1:
    results.append(f"ERREUR (ligne 289) : trouve {count1} fois (attendu 1).")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (ligne 289) : mention du multiplicateur retiree.")

old2 = "<p><strong>SUPER LIKE</strong> sends out extra Wilds carrying its own multiplier.</p>"
new2 = "<p><strong>SUPER LIKE</strong> sends out extra Wilds to the grid.</p>"
count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (ligne 368) : trouve {count2} fois (attendu 1).")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (ligne 368) : mention du multiplicateur retiree.")

old3 = "<p>Possible multiplier values for MATCH and SUPER LIKE are: 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 200x.</p>"
new3 = "<p>Possible multiplier values for MATCH are: 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 200x.</p>"
count3 = content.count(old3)
if count3 != 1:
    results.append(f"ERREUR (ligne 369) : trouve {count3} fois (attendu 1).")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (ligne 369) : ne mentionne plus que MATCH pour cette echelle.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
