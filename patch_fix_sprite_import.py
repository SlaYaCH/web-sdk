path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = "import { App, Text, REM, Container, Rectangle } from 'pixi-svelte';"
new = "import { App, Text, REM, Container, Rectangle, Sprite } from 'pixi-svelte';"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Sprite importe depuis pixi-svelte.")
