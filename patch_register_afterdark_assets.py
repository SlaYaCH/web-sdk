path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

marker = "\theartBullet: {"
count = marker_count = content.count(marker)
if marker_count != 1:
    print(f"ERREUR : marqueur d'ancrage trouve {marker_count} fois (attendu 1).")
else:
    new_entries = """	afterDarkHeartDisplay: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/afterdark_heart_display.png', import.meta.url).href,
	},
	duelPlus2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus2.png', import.meta.url).href,
	},
	duelPlus3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus3.png', import.meta.url).href,
	},
	duelPlus4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus4.png', import.meta.url).href,
	},
	duel5x: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_5x.png', import.meta.url).href,
	},
	matchPlus3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/match_plus3.png', import.meta.url).href,
	},
"""
    idx = content.index(marker)
    content = content[:idx] + new_entries + content[idx:]
    with open(path, "w") as f:
        f.write(content)
    print("OK : 6 nouveaux assets After Dark enregistres.")
