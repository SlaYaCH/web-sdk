path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	introScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/intro_screen.png', import.meta.url).href,
	},
"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : entree introScreen trouvee {count} fois (attendu 1).")
else:
    content = content.replace(old, "", 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : entree introScreen inutilisee supprimee, plus d'erreur 404 au chargement.")
