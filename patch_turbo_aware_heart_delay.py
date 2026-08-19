path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "import { getContext } from '../game/context';"
new1 = "import { getContext } from '../game/context';\n\timport { stateBet } from 'state-shared';"
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (import stateBet) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (import stateBet)")

old2 = "const BASE_DELAY = 900; // laisse le temps aux rouleaux de finir de se poser"
new2 = """const BASE_DELAY = 900; // laisse le temps aux rouleaux de finir de se poser (vitesse normale)
	const effectiveDelay = () => BASE_DELAY / (stateBet.isSuperTurbo ? 4 : stateBet.isTurbo ? 2 : 1);"""
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (effectiveDelay) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (effectiveDelay ajoute, proportionnel a turbo/super turbo)")

old3 = "await new Promise((r) => setTimeout(r, BASE_DELAY));"
new3 = "await new Promise((r) => setTimeout(r, effectiveDelay()));"
n = content.count(old3)
if n != 1:
    results.append(f"ERREUR (usage) : {n} fois.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (usage) : delai reduit automatiquement en turbo/super turbo.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
