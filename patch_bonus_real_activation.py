path = "apps/louvo/src/components/LouvoBonusMenu.svelte"
with open(path, "r") as f:
    content = f.read()

old_options = """	const OPTIONS = [
		{ key: 'date', confirmKey: 'date', desc: 'Chance x5 de déclencher un bonus', mult: 3.0 },
		{ key: 'match', confirmKey: 'match', desc: 'Garantit des symboles MATCH à chaque tour', mult: 60.0 },
		{ key: 'superlike', confirmKey: 'superlike', desc: 'Garantit un Super Like à chaque tour', mult: 60.0 },
		{ key: 'speeddating', confirmKey: 'speeddating', desc: '10 tours gratuits, palier Speed Dating', mult: 80.0 },
		{ key: 'afterdark', confirmKey: 'afterdark', desc: '10 tours gratuits, palier After Dark', mult: 150.0 },
	];"""
new_options = """	const OPTIONS = [
		{ key: 'date', confirmKey: 'date', modeKey: 'MATCH_BOOST', desc: 'Chance x5 de déclencher un bonus', mult: 3.0 },
		{ key: 'match', confirmKey: 'match', modeKey: 'MATCH_FRENZY', desc: 'Garantit des symboles MATCH à chaque tour', mult: 60.0 },
		{ key: 'superlike', confirmKey: 'superlike', modeKey: 'LIKE_STORM', desc: 'Garantit un Super Like à chaque tour', mult: 60.0 },
		{ key: 'speeddating', confirmKey: 'speeddating', modeKey: 'BONUS_SPEED_DATING', desc: '10 tours gratuits, palier Speed Dating', mult: 80.0 },
		{ key: 'afterdark', confirmKey: 'afterdark', modeKey: 'BONUS_AFTER_DARK', desc: '10 tours gratuits, palier After Dark', mult: 150.0 },
	];"""

old_confirm = """	// Renvoie sur le vrai systeme d'achat (garanti fonctionnel)
	const onConfirm = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		confirming = false;
		stateModal.modal = { name: 'buyBonus' };
	};"""
new_confirm = """	// Active directement le vrai mode (cle deduite de config.ts, a confirmer)
	const onConfirm = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		confirming = false;
		stateBet.activeBetModeKey = option.modeKey;
	};"""

missing = [n for n, o in [("options", old_options), ("confirm", old_confirm)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_options, new_options, 1)
    content = content.replace(old_confirm, new_confirm, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les cartes activent maintenant directement le vrai mode correspondant.")
