path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/louvo_intro_screen.png', import.meta.url).href,
	},"""
new = """	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/intro_screen.png', import.meta.url).href,
	},"""

if old not in content:
    print("ERREUR : ancre introuvable (deja corrige ?).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : pointe maintenant vers intro_screen.png (le vrai nom du fichier).")
