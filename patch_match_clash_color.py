path = "apps/louvo/src/components/MatchDuelClash.svelte"
with open(path, "r") as f:
    content = f.read()

old1 = "style={{ fontFamily: 'gold', fontSize: FONT_SIZE }}"
new1 = "style={{ fontFamily: 'gold', fontSize: FONT_SIZE, fill: 0xff2d6a }}"

old2 = "style={{ fontFamily: 'gold', fontSize: WINNER_FONT_SIZE }}"
new2 = "style={{ fontFamily: 'gold', fontSize: WINNER_FONT_SIZE, fill: 0xff2d6a }}"

count = content.count(old1) + content.count(old2)
if count == 0:
    print("ERREUR : ancres introuvables.")
else:
    content = content.replace(old1, new1)
    content = content.replace(old2, new2)
    with open(path, "w") as f:
        f.write(content)
    print(f"OK : couleur rose/rouge appliquee ({count} occurrence(s)) - si ca ne change rien visuellement, la police n'est pas teintable.")
