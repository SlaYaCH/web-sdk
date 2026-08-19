path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "const effectiveDelay = () => BASE_DELAY / (stateBet.isSuperTurbo ? 4 : stateBet.isTurbo ? 2 : 1);"
new1 = """const effectiveDelay = () => BASE_DELAY / (stateBet.isSuperTurbo ? 4 : stateBet.isTurbo ? 2 : 1);
	// Attente robuste : au lieu de deviner un minuteur, on verifie l'etat
	// REEL de chaque rouleau (comme pour l'anticipation) - garantit que les
	// coeurs ne partent JAMAIS pendant qu'un rouleau tourne encore.
	const waitForAllReelsStopped = async () => {
		while (context.stateGame.board.some((reel) => reel.reelState.motion !== 'stopped')) {
			await new Promise((r) => setTimeout(r, 50));
		}
	};"""
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (fonction attente) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (fonction waitForAllReelsStopped ajoutee)")

old2 = "await new Promise((r) => setTimeout(r, effectiveDelay()));"
new2 = "await waitForAllReelsStopped();\n\t\t\t\tawait new Promise((r) => setTimeout(r, effectiveDelay()));"
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (usage) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (attend vraiment tous les rouleaux avant le delai)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
