# --- assets.ts : enregistrer les 2 cartes et 4 confirmations manquantes ---
path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old_anchor = """	louvoCard_superlike: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_superlike.png', import.meta.url).href,
	},"""
new_assets = old_anchor + """
	louvoCard_speeddating: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_speeddating.png', import.meta.url).href,
	},
	louvoCard_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_afterdark.png', import.meta.url).href,
	},
	louvoConfirm_match: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_match.png', import.meta.url).href,
	},
	louvoConfirm_superlike: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_superlike.png', import.meta.url).href,
	},
	louvoConfirm_date: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_date.png', import.meta.url).href,
	},
	louvoConfirm_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_afterdark.png', import.meta.url).href,
	},"""

if old_anchor not in content:
    print("ERREUR assets.ts : ancre introuvable.")
else:
    content = content.replace(old_anchor, new_assets, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : 6 nouveaux assets enregistres (2 cartes + 4 confirmations).")
