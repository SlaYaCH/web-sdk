path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = "import { App, Text, REM } from 'pixi-svelte';"
new = "import { App, Text, REM, Container } from 'pixi-svelte';"

if old not in content:
    print("ERREUR : ancre introuvable (peut-etre deja corrige, ou import different).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Container ajoute a l'import pixi-svelte dans Game.svelte.")
