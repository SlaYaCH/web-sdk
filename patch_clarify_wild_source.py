path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = "<p><strong>WILD</strong> substitutes for all symbols on the paytable.</p>"
new = "<p><strong>WILD</strong> substitutes for all symbols on the paytable. Wilds only appear on the grid through the SUPER LIKE feature.</p>"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : precise que les wilds ne viennent que de SUPER LIKE.")
