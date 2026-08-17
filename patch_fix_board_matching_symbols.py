import json

path = "apps/louvo/src/stories/data/base_books.ts"
with open(path, "r") as f:
    raw = f.read()

prefix = "export default"
assert raw.strip().startswith(prefix)
body = raw.strip()[len(prefix):].strip()
if body.endswith(";"):
    body = body[:-1].strip()

data = json.loads(body)

board = data[0]["events"][0]["board"]
print("Avant, index 3 de chaque rouleau :", [board[r][3] for r in range(5)])

for reel_index in range(5):
    board[reel_index][3] = {"name": "H5"}

print("Apres, index 3 de chaque rouleau :", [board[r][3] for r in range(5)])

new_body = json.dumps(data, indent=2)
new_content = f"{prefix} {new_body};\n"

with open(path, "w") as f:
    f.write(new_content)

print("OK : les 5 rouleaux ont maintenant H5 a l'indice 3 (= rangee visible du milieu, row 2).")
