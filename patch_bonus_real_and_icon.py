# --- assets.ts : enregistrer l'icone bonus ---
path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	uiSettingsMenu: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/settings_menu.png', import.meta.url).href,
	},"""
new = old + """
	uiBonusIcon: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/bonus_icon.png', import.meta.url).href,
	},"""

if old not in content:
    print("ERREUR assets.ts : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : uiBonusIcon enregistre.")
