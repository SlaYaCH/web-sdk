path = "apps/louvo/src/components/Board.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const reelSymbol = context.stateGame.board[position.reel].reelState.symbols[position.row];"
new = "const reelSymbol = context.stateGame.board[position.reel].reelState.symbols[position.row + 1];"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1) - verification manuelle necessaire.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : decalage +1 applique, comme pour Super Like (evite la case de padding invisible).")
