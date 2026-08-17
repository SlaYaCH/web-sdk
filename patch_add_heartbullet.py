path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	K: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_icon.png', import.meta.url).href,
	},
	S: {"""
new = """	K: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_icon.png', import.meta.url).href,
	},
	heartBullet: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_heart_bullet.png', import.meta.url).href,
	},
	S: {"""

if old not in content:
    print("ERREUR : ancre introuvable - il faudra me recoller le fichier complet.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : heartBullet ajoute pour de vrai cette fois.")
