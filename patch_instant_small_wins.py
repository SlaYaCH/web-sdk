path = "apps/louvo/src/components/Win.svelte"
with open(path, "r") as f:
    content = f.read()

old = """						onmount={async () => {
								await startCountUp();
								await waitForTimeout(300);
								if (!stateBet.stopOnWin) {
									await waitForTimeout(duration);
									oncomplete();
								}
								// Si stopOnWin est actif, reste affiche jusqu'a un clic manuel
								// (PressToContinue) ou le prochain spin.
							}}"""
new = """						onmount={async () => {
								if (isBigWin) {
									// A partir de BIG WIN : compte depuis zero, reste affiche
									// le temps prevu pour la mise en scene.
									await startCountUp();
									await waitForTimeout(300);
									if (!stateBet.stopOnWin) {
										await waitForTimeout(duration);
										oncomplete();
									}
								} else {
									// En dessous de BIG WIN : affichage instantane du montant
									// final (pas de comptage depuis zero) et enchainement
									// immediat sur le tour suivant, sans aucune attente.
									finishCountUp();
									if (!stateBet.stopOnWin) {
										oncomplete();
									}
								}
								// Si stopOnWin est actif, reste affiche jusqu'a un clic manuel
								// (PressToContinue) ou le prochain spin, quel que soit le palier.
							}}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : gains en dessous de BIG WIN affiches instantanement et enchainent direct, big win+ garde le comptage.")
