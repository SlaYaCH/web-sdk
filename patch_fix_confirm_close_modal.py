path = "apps/louvo/src/components/LouvoBonusMenu.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const onConfirm = () => {
		if (!confirming) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateBet.activeBetModeKey = confirming.modeKey;
		confirming = null;
	};"""
new = """	const onConfirm = () => {
		if (!confirming) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateBet.activeBetModeKey = confirming.modeKey;
		confirming = null;
		stateModal.modal = null;
	};"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : la fenetre se ferme maintenant vraiment apres confirmation, plus de retour sur la liste d'achats.")
