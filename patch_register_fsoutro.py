path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = "\tfsIntro: {"
new = """	fsOutroNumber: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/fsIntro/fs_screen.webp', import.meta.url).href,
			atlas: new URL('../../assets/spines/fsIntro/fs_screen.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/fsIntro/fs_total_number.json', import.meta.url).href,
		},
	},
	fsIntro: {"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : fsOutroNumber enregistre (reutilise fs_screen.webp/atlas + fs_total_number.json).")
