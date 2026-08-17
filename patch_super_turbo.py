# --- 1) state-shared : ajouter isSuperTurbo + l'utiliser dans timeScale (additif, sans danger pour les autres jeux) ---
path1 = "packages/state-shared/src/stateBet.svelte.ts"
with open(path1, "r") as f:
    c1 = f.read()

old1a = "\tisSpaceHold: false,\n\tisTurbo: false,\n});"
new1a = "\tisSpaceHold: false,\n\tisTurbo: false,\n\tisSuperTurbo: false,\n});"

old1b = "const timeScale = () => (stateBet.isTurbo ? 2 : 1);"
new1b = "const timeScale = () => (stateBet.isSuperTurbo ? 4 : stateBet.isTurbo ? 2 : 1);"

missing1 = [n for n, o in [("state", old1a), ("timeScale", old1b)] if o not in c1]
if missing1:
    print("ERREUR stateBet.svelte.ts : ancre(s) introuvable(s) :", missing1)
else:
    c1 = c1.replace(old1a, new1a, 1)
    c1 = c1.replace(old1b, new1b, 1)
    with open(path1, "w") as f:
        f.write(c1)
    print("OK : isSuperTurbo ajoute a stateBet (state-shared), timeScale passe a x4 quand actif.")

# --- 2) constants.ts (Louvo uniquement) : vitesses de rouleaux encore plus rapides ---
path2 = "apps/louvo/src/game/constants.ts"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 5,
	reelSpinSpeed: 5,
	reelBounceSizeMulti: 0.05,
};"""
new2 = old2 + """

export const SPIN_OPTIONS_SUPERFAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 9,
	reelSpinSpeed: 9,
	reelBounceSizeMulti: 0.02,
};"""

if old2 not in c2:
    print("ERREUR constants.ts : ancre introuvable.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    print("OK : SPIN_OPTIONS_SUPERFAST ajoute (Louvo uniquement).")

# --- 3) stateGame.svelte.ts (Louvo uniquement) : choisir SUPERFAST quand actif ---
path3 = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path3, "r") as f:
    c3 = f.read()

old3 = """reel.reelState.spinOptions = () =>
		reel.reelState.spinType === 'fast' ? SPIN_OPTIONS_FAST : SPIN_OPTIONS_DEFAULT;"""
new3 = """reel.reelState.spinOptions = () => {
		if (reel.reelState.spinType !== 'fast') return SPIN_OPTIONS_DEFAULT;
		return stateBet.isSuperTurbo ? SPIN_OPTIONS_SUPERFAST : SPIN_OPTIONS_FAST;
	};"""

if old3 not in c3:
    print("ERREUR stateGame.svelte.ts : ancre introuvable.")
else:
    c3 = c3.replace(old3, new3, 1)
    with open(path3, "w") as f:
        f.write(c3)
    print("OK : stateGame utilise SUPERFAST quand isSuperTurbo est actif.")
