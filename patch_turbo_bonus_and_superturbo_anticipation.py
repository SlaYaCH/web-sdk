# --- 1) Desactiver turbo/super turbo au declenchement d'un bonus ---
path1 = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path1, "r") as f:
    c1 = f.read()

old1 = """	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });"""
new1 = """	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		stateBetDerived.updateIsTurbo(false, { persistent: true });
		stateBet.isSuperTurbo = false;
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });"""

if old1 not in c1:
    print("ERREUR bookEventHandlerMap.ts : ancre introuvable.")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    print("OK : turbo et super turbo se coupent au declenchement d'un bonus.")

# --- 2) Super Turbo court-circuite l'anticipation (garde tout en 'fast') ---
path2 = "packages/utils-slots/src/createEnhanceBoardSpin.ts"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """		const getSpinType = ({
			noStop,
			isAnticipated,
		}: {
			noStop: boolean;
			isAnticipated: boolean;
		}) => {
			if (isAnticipated) return 'anticipated';
			if (noStop) return 'normal';
			return globalSpinType;
		};"""
new2 = """		const getSpinType = ({
			noStop,
			isAnticipated,
		}: {
			noStop: boolean;
			isAnticipated: boolean;
		}) => {
			if (isAnticipated && !stateBet.isSuperTurbo) return 'anticipated';
			if (noStop) return 'normal';
			return globalSpinType;
		};"""

if old2 not in c2:
    print("ERREUR createEnhanceBoardSpin.ts : ancre introuvable.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    print("OK : le Super Turbo ignore desormais le suspense d'anticipation (reste en vitesse rapide constante).")
