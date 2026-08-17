path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { Container, Sprite, Text } from 'pixi-svelte';"
new_import = "import { Container, Sprite, Text, Rectangle } from 'pixi-svelte';"

replacements = [
    ('<Sprite width={100} height={100} alpha={0.001} />',
     '<Rectangle anchor={0.5} width={100} height={100} alpha={0.001} backgroundColor={0x000000} />'),
    ('<Sprite width={50} height={40} alpha={0.001} />\n\t</Container>\n\n\t<!-- Fleche bas',
     '<Rectangle anchor={0.5} width={50} height={40} alpha={0.001} backgroundColor={0x000000} />\n\t</Container>\n\n\t<!-- Fleche bas'),
    ('<Sprite width={50} height={40} alpha={0.001} />\n\t</Container>\n\n\t<!-- Autoplay',
     '<Rectangle anchor={0.5} width={50} height={40} alpha={0.001} backgroundColor={0x000000} />\n\t</Container>\n\n\t<!-- Autoplay'),
    ('<Sprite width={70} height={70} alpha={0.001} />',
     '<Rectangle anchor={0.5} width={70} height={70} alpha={0.001} backgroundColor={0x000000} />'),
    ('<Sprite width={180} height={180} alpha={0.001} />',
     '<Rectangle anchor={0.5} width={180} height={180} alpha={0.001} backgroundColor={0x000000} />'),
]

missing = [old for old, new in replacements if old not in content]
if "import { Container, Sprite, Text } from 'pixi-svelte';" not in content:
    missing.append("import")

if missing:
    print("ERREUR : ancre(s) introuvable(s) :", len(missing), "sur", len(replacements) + 1)
else:
    content = content.replace(old_import, new_import, 1)
    for old, new in replacements:
        content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les 5 zones cliquables ont maintenant de vraies dimensions (Rectangle au lieu de Sprite sans image).")
