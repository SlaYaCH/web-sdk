path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = """	const flyTo = (index: number) =>
		new Promise<void>((resolve) => {
			const target = targets[index];
			const duration = 550;
			const arcHeight = 60 + Math.random() * 30;
			const start = performance.now();"""
new1 = """	const flyTo = (index: number) =>
		new Promise<void>((resolve) => {
			const target = targets[index];
			const duration = 550;
			const arcHeight = 60 + Math.random() * 30;
			const start = performance.now();

			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up' });"""

count1 = content.count(old1)
if count1 != 1:
    results.append(f"ERREUR (son vol) : trouve {count1} fois (attendu 1) - verification manuelle necessaire.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (son vol) : sfx_multiplier_up joue au depart de chaque coeur.")

old2 = """						reelSymbol.rawSymbol = { name: 'W', wild: true };
					}
					// Le coeur disparait immediatement"""
new2 = """						reelSymbol.rawSymbol = { name: 'W', wild: true };
					}
					context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
					// Le coeur disparait immediatement"""

count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (son wild) : trouve {count2} fois (attendu 1) - verification manuelle necessaire.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (son wild) : sfx_wild_explode joue exactement quand le wild apparait.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
