path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;"""
new = """	uiBottomBar: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/bottom_bar.png', import.meta.url).href,
	},

	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;"""

if old not in content:
    print("ERREUR assets.ts : ancre introuvable (peut-etre deja fait).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : uiBottomBar enregistre dans assets.ts.")
