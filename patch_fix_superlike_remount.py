path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "\tlet revealReelIndex = $state(0);"
new1 = "\tlet revealReelIndex = $state(0);\n\tlet revealId = $state(0);"
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (revealId) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (revealId ajoute)")

old2 = "\t\trevealReelIndex = emitterEvent.reelIndex;\n\t\tshow = true;"
new2 = "\t\trevealReelIndex = emitterEvent.reelIndex;\n\t\trevealId += 1;\n\t\tshow = true;"
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (increment) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (increment a chaque reveal)")

old3 = "\t\t\t{#if assetKey === 'superlikeReveal'}\n\t\t\t\t<SuperlikeHeartThrow reelIndex={revealReelIndex} positions={likePositions} />\n\t\t\t{/if}"
new3 = "\t\t\t{#if assetKey === 'superlikeReveal'}\n\t\t\t\t{#key revealId}\n\t\t\t\t\t<SuperlikeHeartThrow reelIndex={revealReelIndex} positions={likePositions} />\n\t\t\t\t{/key}\n\t\t\t{/if}"
n = content.count(old3)
if n != 1:
    results.append(f"ERREUR (key) : {n} fois - verification manuelle necessaire.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (key) : force une nouvelle instance a chaque Super Like, l'animation devrait toujours se rejouer.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
