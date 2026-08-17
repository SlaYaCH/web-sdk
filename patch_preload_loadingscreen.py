path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	loadingScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/loading_screen.png', import.meta.url).href,
	},"""
new = """	loadingScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/loading_screen.png', import.meta.url).href,
		preload: true,
	},"""

if old not in content:
    print("ERREUR assets.ts : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : loadingScreen charge maintenant en priorite, comme progressBar - la barre devrait s'animer PAR-DESSUS le fond, pas avant.")
