results = []

# --- 1) REVERT : la banniere Super Like garde bien son multiplicateur ---
path1 = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1 = """			assetKey = emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal';
			// Super Like ne porte plus de multiplicateur (mecanique changee
			// cote Math SDK) - le texte ne s'affiche donc plus que pour MATCH.
			multiplierText = emitterEvent.symbol === 'M' ? `x${emitterEvent.multiplier}` : '';"""
new1 = """			assetKey = emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal';
			multiplierText = `x${emitterEvent.multiplier}`;"""

count1 = c1.count(old1)
if count1 != 1:
    results.append(f"ERREUR (revert banniere) : trouve {count1} fois (attendu 1).")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK (revert banniere) : Super Like affiche de nouveau son multiplicateur (jusqu'a x200).")

# --- 2) Corriger le texte des regles avec la vraie nuance ---
path2 = "apps/louvo/src/components/Game.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2a = "<p>The SUPER LIKE symbol sends out between 1 and 6 Wilds to random empty positions on the grid.</p>"
new2a = "<p>The SUPER LIKE symbol reveals a multiplier and sends out between 1 and 6 Wilds to random empty positions on the grid.</p>"
count2a = c2.count(old2a)
if count2a != 1:
    results.append(f"ERREUR (ligne 289) : trouve {count2a} fois (attendu 1).")
else:
    c2 = c2.replace(old2a, new2a, 1)
    results.append("OK (ligne 289) : nuance retablie (SUPER LIKE revele un multiplicateur).")

old2b = "<p><strong>SUPER LIKE</strong> sends out extra Wilds to the grid.</p>"
new2b = "<p><strong>SUPER LIKE</strong> reveals a multiplier and sends out extra Wilds to the grid.</p>"
count2b = c2.count(old2b)
if count2b != 1:
    results.append(f"ERREUR (ligne 368) : trouve {count2b} fois (attendu 1).")
else:
    c2 = c2.replace(old2b, new2b, 1)
    results.append("OK (ligne 368) : nuance retablie.")

old2c = "<p>Possible multiplier values for MATCH are: 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 200x.</p>"
new2c = "<p>Possible multiplier values for MATCH and SUPER LIKE are: 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 200x.</p>"
count2c = c2.count(old2c)
if count2c != 1:
    results.append(f"ERREUR (ligne 369) : trouve {count2c} fois (attendu 1).")
else:
    c2 = c2.replace(old2c, new2c, 1)
    results.append("OK (ligne 369) : SUPER LIKE reintegre dans la liste (le multiplicateur existe toujours).")

with open(path2, "w") as f:
    f.write(c2)

for r in results:
    print(r)
