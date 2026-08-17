path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = """						context.stateGame.board[pos.reelIndex]?.reelState?.symbols[pos.rowIndex];"""
new = """						context.stateGame.board[pos.reelIndex]?.reelState?.symbols[pos.rowIndex + 1];"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : decalage d'une rangee vers le bas applique.")
