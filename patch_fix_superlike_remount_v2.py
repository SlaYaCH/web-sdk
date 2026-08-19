path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old = "\t\t\trevealReelIndex = emitterEvent.reelIndex;\n\t\t\tshow = true;"
new = "\t\t\trevealReelIndex = emitterEvent.reelIndex;\n\t\t\trevealId += 1;\n\t\t\tshow = true;"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : revealId s'incremente a chaque nouveau reveal.")
