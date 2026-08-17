path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old = "holdMs={15000}"
new = "holdMs={2500}"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : fermeture automatique remise a 2.5s, plus de blocage possible.")
