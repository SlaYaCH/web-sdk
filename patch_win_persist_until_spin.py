path = "apps/louvo/src/components/Win.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = """	context.eventEmitter.subscribeOnMount({
		winShow: () => (show = true),
		winHide: () => (show = false),
		winUpdate: async (emitterEvent) => {"""
new1 = """	context.eventEmitter.subscribeOnMount({
		winShow: () => (show = true),
		winHide: () => (show = false),
		spinStart: () => {
			if (show) oncomplete();
		},
		winUpdate: async (emitterEvent) => {"""

count1 = content.count(old1)
if count1 != 1:
    results.append(f"ERREUR (spinStart) : trouve {count1} fois (attendu 1).")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (spinStart) : ajoute, ferme le gain au prochain spin s'il est encore affiche.")

old2 = """						onmount={async () => {
								await startCountUp();
								await waitForTimeout(300);
								oncomplete();
							}}"""
new2 = """						onmount={async () => {
								await startCountUp();
								await waitForTimeout(300);
								// Reste affiche jusqu'au prochain spin (ou un clic manuel via
								// PressToContinue) - plus de fermeture automatique ici.
							}}"""

count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (onmount) : trouve {count2} fois (attendu 1) - verification manuelle necessaire.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (onmount) : fermeture automatique retiree.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
