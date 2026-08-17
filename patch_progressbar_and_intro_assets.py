path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	loadingScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/loading_screen.png', import.meta.url).href,
	},"""
new = old + """
	progressBar: {
		type: 'sprites',
		src: new URL('../../assets/sprites/progressBar/progressBar.json', import.meta.url).href,
		preload: true,
	},
	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/louvo_intro_screen.png', import.meta.url).href,
	},"""

if old not in content:
    print("ERREUR assets.ts : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : progressBar + louvoIntroScreen enregistres.")
