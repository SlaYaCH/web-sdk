path = "apps/louvo/src/components/LouvoSettingsMenu.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

# 1) Remplacer le onTurbo existant par la version qui coupe aussi super turbo,
#    et ajouter onSuperTurbo juste apres (ancre sur une seule ligne, sans risque)
old_a = "stateBetDerived.updateIsTurbo(!stateBet.isTurbo, { persistent: true });"
new_a = """const next = !stateBet.isTurbo;
		stateBetDerived.updateIsTurbo(next, { persistent: true });
		if (!next) stateBet.isSuperTurbo = false;
	};
	const onSuperTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const next2 = !stateBet.isSuperTurbo;
		stateBet.isSuperTurbo = next2;
		if (next2) stateBetDerived.updateIsTurbo(true, { persistent: true });"""
count_a = content.count(old_a)
if count_a != 1:
    results.append(f"ERREUR (a) : trouve {count_a} fois, attendu 1.")
else:
    content = content.replace(old_a, new_a, 1)
    results.append("OK (a) : onTurbo corrige + onSuperTurbo ajoute.")

# 2) Ajouter superTurboLabel juste apres turboLabel (ancre sur une seule ligne)
old_b = "const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');"
count_b = content.count(old_b)
if count_b != 1:
    results.append(f"ERREUR (b) : trouve {count_b} fois, attendu 1.")
else:
    new_b = old_b + "\n\tconst superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO : ACTIF' : 'SUPER TURBO : COUPÉ');"
    content = content.replace(old_b, new_b, 1)
    results.append("OK (b) : superTurboLabel ajoute.")

# 3) Faire pointer la ligne SUPER TURBO vers le bon label + le bon handler (ancre sur une seule ligne)
old_c = "{ label: 'SUPER TURBO', onpress: onTurbo },"
count_c = content.count(old_c)
if count_c != 1:
    results.append(f"ERREUR (c) : trouve {count_c} fois, attendu 1.")
else:
    new_c = "{ label: superTurboLabel, onpress: onSuperTurbo },"
    content = content.replace(old_c, new_c, 1)
    results.append("OK (c) : ligne SUPER TURBO branchee sur son propre etat.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
