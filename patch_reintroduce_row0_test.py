import json

path = "apps/louvo/src/stories/data/base_books.ts"
with open(path, "r") as f:
    raw = f.read()

prefix = "export default"
body = raw.strip()[len(prefix):].strip()
if body.endswith(";"):
    body = body[:-1].strip()
data = json.loads(body)

line0 = [0, 0, 0, 0, 0]   # horizontale sur la rangee du HAUT (le cas qui bloquait)
line3 = [2, 2, 2, 2, 2]   # deja en place, inchangee

SYM_LINE0 = "L1"
SYM_LINE3 = "H5"
FILLER_CHOICES = ["H3", "H4", "L4", "L2"]

board = data[0]["events"][0]["board"]

for reel in range(5):
    idx_line0 = line0[reel] + 1
    idx_line3 = line3[reel] + 1
    for raw_idx in range(7):
        if raw_idx == idx_line0:
            board[reel][raw_idx] = {"name": SYM_LINE0}
        elif raw_idx == idx_line3:
            board[reel][raw_idx] = {"name": SYM_LINE3}
        else:
            board[reel][raw_idx] = {"name": FILLER_CHOICES[(reel + raw_idx) % len(FILLER_CHOICES)]}

has_wild = any(cell.get("wild") or cell.get("name") == "W" for reel in board for cell in reel)
print("Reste-t-il un wild ?", has_wild)

win_info = data[0]["events"][2]
win_info["wins"] = [
    {
        "symbol": SYM_LINE0, "kind": 3, "win": 10,
        "positions": [{"reel": r, "row": line0[r]} for r in range(5)],
        "meta": {"lineIndex": 1, "multiplier": 1, "winWithoutMult": 10, "globalMult": 1, "lineMultiplier": 1},
    },
    {
        "symbol": SYM_LINE3, "kind": 3, "win": 20,
        "positions": [{"reel": r, "row": line3[r]} for r in range(5)],
        "meta": {"lineIndex": 3, "multiplier": 1, "winWithoutMult": 20, "globalMult": 1, "lineMultiplier": 1},
    },
]
win_info["totalWin"] = 30
data[0]["events"][3]["amount"] = 30
data[0]["events"][4]["amount"] = 30
data[0]["events"][5]["amount"] = 30
data[0]["payoutMultiplier"] = 30

new_body = json.dumps(data, indent=2)
with open(path, "w") as f:
    f.write(f"{prefix} {new_body};\n")

print("OK : book reconstruit avec une ligne sur la rangee du HAUT (row 0) + une horizontale au milieu, pour tester le vrai correctif.")
