path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old = "<Container x={BAR_WIDTH * 0.5} y={-BAR_HEIGHT * 0.5}>"
new = "<Container x={0} y={-BAR_HEIGHT * 0.5}>"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : le decalage en double est corrige, la barre doit maintenant etre bien centree.")
