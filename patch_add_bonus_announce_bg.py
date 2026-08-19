results = []

# --- 1) Deplacer stateGame.tier plus tot, avant l'ecran d'annonce ---
path1 = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path1, "r") as f:
    c1 = f.read()

old1 = """		stateBetDerived.updateIsTurbo(false, { persistent: true });
		stateBet.isSuperTurbo = false;
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });"""
new1 = """		stateBetDerived.updateIsTurbo(false, { persistent: true });
		stateBet.isSuperTurbo = false;
		stateGame.tier = bookEvent.tier ?? 'speed_dating';
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });"""
n = c1.count(old1)
if n != 1:
    results.append(f"ERREUR (deplacement tier) : {n} fois.")
else:
    c1 = c1.replace(old1, new1, 1)
    results.append("OK (deplacement tier)")

old1b = "\t\t\tstateGame.gameType = 'freegame';\n\t\t\tstateGame.tier = bookEvent.tier ?? 'speed_dating';\n"
new1b = "\t\t\tstateGame.gameType = 'freegame';\n"
n = c1.count(old1b)
if n != 1:
    results.append(f"ERREUR (retrait doublon) : {n} fois.")
else:
    c1 = c1.replace(old1b, new1b, 1)
    results.append("OK (retrait doublon)")

with open(path1, "w") as f:
    f.write(c1)

# --- 2) Ajouter le fond d'annonce specifique au palier ---
path2 = "apps/louvo/src/components/FreeSpinIntro.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = "<FadeContainer {show}>\n\t<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />"
new2 = """<FadeContainer {show}>
	<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />
	<Sprite
		anchor={0.5}
		width={context.stateLayoutDerived.canvasSizes().width}
		height={context.stateLayoutDerived.canvasSizes().height}
		key={context.stateGame.tier === 'after_dark' ? 'afterDarkAnnounce' : 'speedDatingAnnounce'}
	/>"""
n = c2.count(old2)
if n != 1:
    results.append(f"ERREUR (fond annonce) : {n} fois - verification manuelle necessaire.")
else:
    c2 = c2.replace(old2, new2, 1)
    results.append("OK (fond annonce ajoute, bascule speedDating/afterDark selon le palier)")

with open(path2, "w") as f:
    f.write(c2)

for r in results:
    print(r)
