path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/intro_screen.png', import.meta.url).href,
	},"""
new = """	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/louvo_intro_screen.png', import.meta.url).href,
	},"""

count = content.count(old)
if count == 0:
    print("ERREUR : ancre introuvable (verifiez l'indentation reelle).")
elif count > 1:
    print(f"ERREUR : trouvee {count} fois, encore ambigue.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : louvoIntroScreen (et uniquement celle-la) pointe vers louvo_intro_screen.png.")
