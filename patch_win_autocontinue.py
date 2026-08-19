path = "apps/louvo/src/components/Win.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "\tfrom '../game/context';"
new1 = old1
old1b = "import { getContext } from '../game/context';"
new1b = "import { getContext } from '../game/context';\n\timport { stateBet } from 'state-shared';"
count1 = content.count(old1b)
if count1 != 1:
    results.append(f"ERREUR (import stateBet) : trouve {count1} fois.")
else:
    content = content.replace(old1b, new1b, 1)
    results.append("OK (import stateBet)")

old2 = """						onmount={async () => {
								await startCountUp();
								await waitForTimeout(300);
								// Reste affiche jusqu'au prochain spin (ou un clic manuel via
								// PressToContinue) - plus de fermeture automatique ici.
							}}"""
new2 = """						onmount={async () => {
								await startCountUp();
								await waitForTimeout(300);
								if (!stateBet.stopOnWin) {
									await waitForTimeout(duration);
									oncomplete();
								}
								// Si "stopOnWin" est actif, reste affiche jusqu'a un clic
								// manuel (PressToContinue) ou le prochain spin.
							}}"""
count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (onmount) : trouve {count2} fois - verification manuelle necessaire.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (onmount) : auto-continue apres presentDuration, sauf si stopOnWin actif.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
