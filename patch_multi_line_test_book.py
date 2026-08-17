import json

path = "apps/louvo/src/stories/data/base_books.ts"
with open(path, "r") as f:
    raw = f.read()

prefix = "export default"
body = raw.strip()[len(prefix):].strip()
if body.endswith(";"):
    body = body[:-1].strip()
data = json.loads(body)

# Lignes cibles (indices de rangee visible, 0-4, par rouleau 0-4)
line3  = [2,2,2,2,2]   # horizontale (deja en place, H5)
line6  = [0,1,0,1,0]   # zigzag
line13 = [4,3,4,3,4]   # "pyramide" (W peu profond, rangees 3-4)

SYM_LINE3 = "H5"
SYM_LINE6 = "L1"
SYM_LINE13 = "L2"
FILLER_CHOICES = ["H3", "H4", "L4"]  # jamais W, varie pour eviter des matchs non voulus

board = data[0]["events"][0]["board"]

for reel in range(5):
    # index brut = rangee visible + 1 (padding au-dessus)
    idx_line6 = line6[reel] + 1
    idx_line3 = line3[reel] + 1
    idx_line13 = line13[reel] + 1

    for raw_idx in range(7):
        if raw_idx == idx_line3:
            board[reel][raw_idx] = {"name": SYM_LINE3}
        elif raw_idx == idx_line6:
            board[reel][raw_idx] = {"name": SYM_LINE6}
        elif raw_idx == idx_line13:
            board[reel][raw_idx] = {"name": SYM_LINE13}
        else:
            board[reel][raw_idx] = {"name": FILLER_CHOICES[(reel + raw_idx) % len(FILLER_CHOICES)]}

# Verifier qu'il ne reste plus aucun wild
has_wild = any(cell.get("wild") or cell.get("name") == "W" for reel in board for cell in reel)
print("Reste-t-il un wild ?", has_wild)

# Reconstruire les 3 gains dans winInfo (index 2)
win_info = data[0]["events"][2]
win_info["wins"] = [
    {
        "symbol": SYM_LINE3, "kind": 3, "win": 20,
        "positions": [{"reel": r, "row": line3[r]} for r in range(5)],
        "meta": {"lineIndex": 3, "multiplier": 1, "winWithoutMult": 20, "globalMult": 1, "lineMultiplier": 1},
    },
    {
        "symbol": SYM_LINE6, "kind": 3, "win": 2,
        "positions": [{"reel": r, "row": line6[r]} for r in range(5)],
        "meta": {"lineIndex": 6, "multiplier": 1, "winWithoutMult": 2, "globalMult": 1, "lineMultiplier": 1},
    },
    {
        "symbol": SYM_LINE13, "kind": 3, "win": 2,
        "positions": [{"reel": r, "row": line13[r]} for r in range(5)],
        "meta": {"lineIndex": 13, "multiplier": 1, "winWithoutMult": 2, "globalMult": 1, "lineMultiplier": 1},
    },
]
win_info["totalWin"] = 24

# Aligner les montants affiches ailleurs sur ce nouveau total
data[0]["events"][3]["amount"] = 24  # setWin
data[0]["events"][4]["amount"] = 24  # setTotalWin
data[0]["events"][5]["amount"] = 24  # finalWin
data[0]["payoutMultiplier"] = 24

new_body = json.dumps(data, indent=2)
with open(path, "w") as f:
    f.write(f"{prefix} {new_body};\n")

print("OK : plateau reconstruit avec 3 lignes non chevauchantes (horizontale/zigzag/pyramide), aucun wild, gains alignes sur 24 au total.")
