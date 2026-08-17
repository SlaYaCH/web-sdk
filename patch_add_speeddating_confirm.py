# --- assets.ts ---
path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	louvoConfirm_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_afterdark.png', import.meta.url).href,
	},"""
new = old + """
	louvoConfirm_speeddating: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_speeddating.png', import.meta.url).href,
	},"""

if old not in content:
    print("ERREUR assets.ts : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : louvoConfirm_speeddating enregistre.")

# --- LouvoBonusMenu.svelte : donner une vraie confirmKey a speeddating ---
path = "apps/louvo/src/components/LouvoBonusMenu.svelte"
with open(path, "r") as f:
    content = f.read()

old = "{ key: 'speeddating', confirmKey: null, desc: '10 tours gratuits, palier Speed Dating', mult: 80.0 },"
new = "{ key: 'speeddating', confirmKey: 'speeddating', desc: '10 tours gratuits, palier Speed Dating', mult: 80.0 },"

if old not in content:
    print("ERREUR LouvoBonusMenu.svelte : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Speed Dating utilise maintenant sa vraie confirmation.")
