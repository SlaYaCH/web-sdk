import json

path = "apps/louvo/src/stories/data/base_books.ts"
with open(path, "r") as f:
    raw = f.read()

prefix = "export default"
body = raw.strip()[len(prefix):].strip()
if body.endswith(";"):
    body = body[:-1].strip()
data = json.loads(body)

line3  = [2,2,2,2,2]   # horizontale
line13 = [4,3,4,3,4]   # deja confirmee OK
line9  = [3,4,3,4,3]   # remplace line6, evite la rangee 0

SYM_LINE3 = "H5"
SYM_LINE13 = "L2"
SYM_LINE9 = "L1"
FILLER_CHOICES = ["H3", "H4", "L4"]

board = data[0]["events"][0]["board"]

for reel in range(5):
    idx_line3 = line3[reel] + 1
    idx_line13 = line13[reel] + 1
    idx_line9 = line9[reel] + 1

    for raw_idx in range(7):
        if raw_idx == idx_line3:
            board[reel][raw_idx] = {"name": SYM_LINE3}
        elif raw_idx == idx_line13:
            board[reel][raw_idx] = {"name": SYM_LINE13}
        elif raw_idx == idx_line9:
            board[reel][raw_idx] = {"name": SYM_LINE9}
        else:
            board[reel][raw_idx] = {"name": FILLER_CHOICES[(reel + raw_idx) % len(FILLER_CHOICES)]}

has_wild = any(cell.get("wild") or cell.get("name") == "W" for reel in board for cell in reel)
print("Reste-t-il un wild ?", has_wild)

win_info = data[0]["events"][2]
win_info["wins"] = [
    {
        "symbol": SYM_LINE3, "kind": 3, "win": 20,
        "positions": [{"reel": r, "row": line3[r]} for r in range(5)],
        "meta": {"lineIndex": 3, "multiplier": 1, "winWithoutMult": 20, "globalMult": 1, "lineMultiplier": 1},
    },
    {
        "symbol": SYM_LINE13, "kind": 3, "win": 2,
        "positions": [{"reel": r, "row": line13[r]} for r in range(5)],
        "meta": {"lineIndex": 13, "multiplier": 1, "winWithoutMult": 2, "globalMult": 1, "lineMultiplier": 1},
    },
    {
        "symbol": SYM_LINE9, "kind": 3, "win": 2,
        "positions": [{"reel": r, "row": line9[r]} for r in range(5)],
        "meta": {"lineIndex": 9, "multiplier": 1, "winWithoutMult": 2, "globalMult": 1, "lineMultiplier": 1},
    },
]
win_info["totalWin"] = 24
data[0]["events"][3]["amount"] = 24
data[0]["events"][4]["amount"] = 24
data[0]["events"][5]["amount"] = 24
data[0]["payoutMultiplier"] = 24

new_body = json.dumps(data, indent=2)
with open(path, "w") as f:
    f.write(f"{prefix} {new_body};\n")

print("OK : plateau reconstruit avec 3 lignes (rangees 2/3/4 uniquement, jamais 0), aucun wild.")
