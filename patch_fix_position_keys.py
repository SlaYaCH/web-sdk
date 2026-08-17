path = "apps/louvo/src/stories/data/base_books.ts"
with open(path, "r") as f:
    content = f.read()

old = """            "positions": [
              { "reelIndex": 0, "rowIndex": 2 },
              { "reelIndex": 1, "rowIndex": 2 },
              { "reelIndex": 2, "rowIndex": 2 },
              { "reelIndex": 3, "rowIndex": 2 },
              { "reelIndex": 4, "rowIndex": 2 }
            ],"""
new = """            "positions": [
              { "reel": 0, "row": 2 },
              { "reel": 1, "row": 2 },
              { "reel": 2, "row": 2 },
              { "reel": 3, "row": 2 },
              { "reel": 4, "row": 2 }
            ],"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois) - le fichier a peut-etre change entre temps, verification manuelle necessaire.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : positions corrigees (reel/row au lieu de reelIndex/rowIndex).")
