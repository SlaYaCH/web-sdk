path = "apps/louvo/src/components/LouvoSettingsMenu.svelte"
with open(path, "r") as f:
    content = f.read()

old_handlers = """	// Turbo / Super Turbo : un seul niveau de turbo existe dans ce moteur
	const onTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateBetDerived.updateIsTurbo(!stateBet.isTurbo, { persistent: true });
	};"""
new_handlers = """	const onTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const next = !stateBet.isTurbo;
		stateBetDerived.updateIsTurbo(next, { persistent: true });
		if (!next) stateBet.isSuperTurbo = false;
	};
	const onSuperTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const next = !stateBet.isSuperTurbo;
		stateBet.isSuperTurbo = next;
		if (next) stateBetDerived.updateIsTurbo(true, { persistent: true });
	};"""

old_rows = """	const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');
	const ROWS = $derived([
		{ label: soundLabel, onpress: onSound },
		{ label: 'MUSIQUE', onpress: onMusic },
		{ label: turboLabel, onpress: onTurbo },
		{ label: 'SUPER TURBO', onpress: onTurbo },
		{ label: 'INFO / RÈGLES', onpress: onInfo },
		{ label: 'FERMER', onpress: onHome },
	]);"""
new_rows = """	const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');
	const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO : ACTIF' : 'SUPER TURBO : COUPÉ');
	const ROWS = $derived([
		{ label: soundLabel, onpress: onSound },
		{ label: 'MUSIQUE', onpress: onMusic },
		{ label: superTurboLabel, onpress: onSuperTurbo },
		{ label: turboLabel, onpress: onTurbo },
		{ label: 'INFO / RÈGLES', onpress: onInfo },
		{ label: 'FERMER', onpress: onHome },
	]);"""

missing = [n for n, o in [("handlers", old_handlers), ("rows", old_rows)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_handlers, new_handlers, 1)
    content = content.replace(old_rows, new_rows, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Super Turbo a maintenant son propre bouton et son propre etat (l'activer allume aussi le Turbo simple ; couper le Turbo simple coupe aussi le Super Turbo).")
