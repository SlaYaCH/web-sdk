path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "import { getSymbolX } from '../game/utils';"
new1 = old1 + "\n\timport { getContext } from '../game/context';"
if old1 not in content:
    results.append("ERREUR (import) : ancre introuvable.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (import) : getContext ajoute.")

old2 = "const props: Props = $props();"
new2 = old2 + "\n\tconst context = getContext();"
count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (context) : trouve {count2} fois (attendu 1).")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (context) : recupere.")

old3 = """				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					resolve();
					// Reste visible (pas de fondu) jusqu'au prochain spin,
					// comme la banniere qui l'accompagne.
				}"""
new3 = """				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					// Le symbole devient WILD exactement au moment ou le coeur
					// touche sa case (pas avant, pas apres).
					const pos = props.positions?.[index];
					if (pos) {
						const reelSymbol =
							context.stateGame.board[pos.reelIndex]?.reelState?.symbols[pos.rowIndex];
						if (reelSymbol) {
							reelSymbol.rawSymbol = { name: 'W', wild: true };
						}
					}
					resolve();
					// Reste visible (pas de fondu) jusqu'au prochain spin,
					// comme la banniere qui l'accompagne.
				}"""

count3 = content.count(old3)
if count3 != 1:
    results.append(f"ERREUR (reveal) : trouve {count3} fois (attendu 1) - le fichier a peut-etre change, verification manuelle necessaire.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (reveal) : symbole transforme en wild exactement a l'atterrissage du coeur.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
