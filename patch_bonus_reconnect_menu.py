path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const onBonus = () => {
		if (bonusDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (bonusActive) {
			stateBet.activeBetModeKey = 'BASE';
		} else {
			stateModal.modal = { name: 'buyBonus' };
		}
	};"""
new = """	const onBonus = () => {
		if (bonusDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (bonusActive) {
			stateBet.activeBetModeKey = 'BASE';
		} else {
			context.eventEmitter.broadcast({ type: 'bonusMenuShow' });
		}
	};"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : le bouton BONUS ouvre maintenant votre vrai ecran (LouvoBonusMenu), plus la fenetre generique.")
