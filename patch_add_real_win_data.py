path = "apps/louvo/src/stories/data/base_books.ts"
with open(path, "r") as f:
    content = f.read()

old = """      {
        "index": 2,
        "type": "winInfo",
        "totalWin": 4220,
        "wins": []
      },"""

new = """      {
        "index": 2,
        "type": "winInfo",
        "totalWin": 4220,
        "wins": [
          {
            "symbol": "H5",
            "kind": 3,
            "win": 4220,
            "positions": [
              { "reelIndex": 0, "rowIndex": 2 },
              { "reelIndex": 1, "rowIndex": 2 },
              { "reelIndex": 2, "rowIndex": 2 },
              { "reelIndex": 3, "rowIndex": 2 },
              { "reelIndex": 4, "rowIndex": 2 }
            ],
            "meta": {
              "lineIndex": 3,
              "multiplier": 7,
              "winWithoutMult": 603,
              "globalMult": 1,
              "lineMultiplier": 7
            }
          }
        ]
      },"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : book de test rempli avec un vrai gain (ligne 3, 5 symboles H5 en ligne droite, positions/lineIndex/montant reels).")
