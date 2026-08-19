path = "apps/louvo/src/components/LouvoSettingsMenu.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = """	const onSuperTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const next2 = !stateBet.isSuperTurbo;
		stateBet.isSuperTurbo = next2;
		if (next2) stateBetDerived.updateIsTurbo(true, { persistent: true });
	};"""
new1 = old1 + """
	const onStopOnWin = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateBet.stopOnWin = !stateBet.stopOnWin;
	};"""
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (onStopOnWin) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (onStopOnWin)")

old2 = """	const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');
	const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO : ACTIF' : 'SUPER TURBO : COUPÉ');
	const BUTTON_ROWS = $derived([
		{ label: turboLabel, onpress: onTurbo },
		{ label: superTurboLabel, onpress: onSuperTurbo },
		{ label: 'INFO / RÈGLES', onpress: onInfo },
		{ label: 'FERMER', onpress: onHome },
	]);"""
new2 = """	const turboLabel = $derived(stateBet.isTurbo ? 'TURBO: ON' : 'TURBO: OFF');
	const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO: ON' : 'SUPER TURBO: OFF');
	const stopOnWinLabel = $derived(stateBet.stopOnWin ? 'STOP ON WIN: ON' : 'STOP ON WIN: OFF');
	const BUTTON_ROWS = $derived([
		{ label: turboLabel, onpress: onTurbo },
		{ label: superTurboLabel, onpress: onSuperTurbo },
		{ label: stopOnWinLabel, onpress: onStopOnWin },
		{ label: 'INFO / RULES', onpress: onInfo },
		{ label: 'CLOSE', onpress: onHome },
	]);"""
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (labels) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (labels + bouton ajoute)")

old3 = "text={`MUSIQUE : ${Math.round(stateSound.volumeValueMusic)}%`}"
new3 = "text={`MUSIC: ${Math.round(stateSound.volumeValueMusic)}%`}"
n = content.count(old3)
if n != 1:
    results.append(f"ERREUR (MUSIQUE) : {n} fois.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (MUSIQUE -> MUSIC)")

old4 = "text={`SON : ${Math.round(stateSound.volumeValueSoundEffect)}%`}"
new4 = "text={`SOUND: ${Math.round(stateSound.volumeValueSoundEffect)}%`}"
n = content.count(old4)
if n != 1:
    results.append(f"ERREUR (SON) : {n} fois.")
else:
    content = content.replace(old4, new4, 1)
    results.append("OK (SON -> SOUND)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
