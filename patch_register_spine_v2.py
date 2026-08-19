path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = "export default {"
new = """export default {
	anticipation: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/anticipation/anticipation.webp', import.meta.url).href,
			rawAtlas: new URL('../../assets/spines/anticipation/anticipation.atlas', import.meta.url).href,
			spine: new URL('../../assets/spines/anticipation/anticipation.json', import.meta.url).href,
		},
	},
	bigwin: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/bigwin/big_wins.webp', import.meta.url).href,
			rawAtlas: new URL('../../assets/spines/bigwin/big_wins.atlas', import.meta.url).href,
			spine: new URL('../../assets/spines/bigwin/mm_bigwin.json', import.meta.url).href,
		},
	},"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : anticipation et bigwin enregistres avec de simples URLs (comme tous les autres sprites).")
