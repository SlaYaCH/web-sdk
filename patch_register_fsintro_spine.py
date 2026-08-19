path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = "export default {"
new = """export default {
	fsIntroNumber: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/fsIntro/fs_screen.webp', import.meta.url).href,
			rawAtlas: new URL('../../assets/spines/fsIntro/fs_screen.atlas', import.meta.url).href,
			spine: new URL('../../assets/spines/fsIntro/fs_screen_number.json', import.meta.url).href,
		},
	},"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : fsIntroNumber enregistre - l'ecran d'annonce de bonus ne devrait plus planter.")
