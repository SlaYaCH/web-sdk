path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import SpecialRevealOverlay from './SpecialRevealOverlay.svelte';"
new_import = old_import + "\nimport DevRevealPanel from './DevRevealPanel.svelte';"

old_tag = "<SpecialRevealOverlay />"
new_tag = "<SpecialRevealOverlay />\n\t\t<DevRevealPanel />"

if old_import not in content or old_tag not in content:
    print("ERREUR : ancre(s) non trouvee(s), rien modifie.")
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_tag, new_tag, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : DevRevealPanel importe et ajoute dans Game.svelte.")
