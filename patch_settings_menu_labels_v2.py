path = "apps/louvo/src/components/LouvoSettingsMenu.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old_a = "const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');"
new_a = "const turboLabel = $derived(stateBet.isTurbo ? 'TURBO: ON' : 'TURBO: OFF');"
n = content.count(old_a)
if n != 1:
    results.append(f"ERREUR (turboLabel) : {n} fois.")
else:
    content = content.replace(old_a, new_a, 1)
    results.append("OK (turboLabel)")

old_b = "const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO : ACTIF' : 'SUPER TURBO : COUPÉ');"
new_b = "const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO: ON' : 'SUPER TURBO: OFF');\n\tconst stopOnWinLabel = $derived(stateBet.stopOnWin ? 'STOP ON WIN: ON' : 'STOP ON WIN: OFF');"
n = content.count(old_b)
if n != 1:
    results.append(f"ERREUR (superTurboLabel) : {n} fois.")
else:
    content = content.replace(old_b, new_b, 1)
    results.append("OK (superTurboLabel + stopOnWinLabel ajoute)")

old_c = "{ label: superTurboLabel, onpress: onSuperTurbo },\n\t\t{ label: 'INFO / RÈGLES', onpress: onInfo },\n\t\t{ label: 'FERMER', onpress: onHome },"
new_c = "{ label: superTurboLabel, onpress: onSuperTurbo },\n\t\t{ label: stopOnWinLabel, onpress: onStopOnWin },\n\t\t{ label: 'INFO / RULES', onpress: onInfo },\n\t\t{ label: 'CLOSE', onpress: onHome },"
n = content.count(old_c)
if n != 1:
    results.append(f"ERREUR (BUTTON_ROWS) : {n} fois - verification manuelle necessaire.")
else:
    content = content.replace(old_c, new_c, 1)
    results.append("OK (BUTTON_ROWS : bouton ajoute + anglais)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
