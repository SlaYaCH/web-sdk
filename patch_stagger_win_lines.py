path = "apps/louvo/src/components/WinLinesDisplay.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	context.eventEmitter.subscribeOnMount({
		winLinesShow: ({ wins }) => {
			const newWins = wins.map((w) => ({ id: nextId++, positions: w.positions, amount: w.win }));
			activeWins = [...activeWins, ...newWins];
		},
	});"""

new = """	const STAGGER_MS = 200;

	context.eventEmitter.subscribeOnMount({
		winLinesShow: async ({ wins }) => {
			for (const w of wins) {
				activeWins = [...activeWins, { id: nextId++, positions: w.positions, amount: w.win }];
				await new Promise((r) => setTimeout(r, STAGGER_MS));
			}
		},
	});"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les lignes multiples s'affichent maintenant l'une apres l'autre (200ms d'ecart), pas simultanement.")
