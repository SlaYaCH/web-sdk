path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	louvoMusic: {
		type: 'audio',
		src: new URL('../../assets/audio/louvo_music.json', import.meta.url).href,
		preload: true,
	},
} as const;"""
new = "} as const;"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1) - verification manuelle necessaire.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : entree louvoMusic retiree pour de bon.")
