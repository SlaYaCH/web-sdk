path = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old_x = "const PANEL_X_FRACS = [0.2285, 0.4306, 0.6292];"
new_x = "const PANEL_X_FRACS = [0.265, 0.4993, 0.7296];"

old_y = "const TITLE_Y_FRAC = 0.2976;"
new_y = "const TITLE_Y_FRAC = 0.4;"

missing = [n for n, o in [("x", old_x), ("y", old_y)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_x, new_x, 1)
    content = content.replace(old_y, new_y, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : positions horizontales recalibrees avec le meme facteur que la barre (fiable), Y descendu davantage.")
