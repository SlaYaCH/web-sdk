path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = "import { UiGameName, ButtonPayTable, ButtonGameRules, ButtonSettings, ButtonSoundSwitch, ButtonMenuClose } from 'components-ui-pixi';"
new = "import { UiGameName } from 'components-ui-pixi';"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : import nettoye, ne reference plus que UiGameName (les boutons generiques ne sont plus utilises de toute facon).")
