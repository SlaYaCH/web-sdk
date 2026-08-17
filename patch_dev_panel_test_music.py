path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	const setTier = (tier: 'basegame' | 'speed_dating' | 'after_dark') => {
		context.stateGame.gameType = tier === 'basegame' ? 'basegame' : 'freegame';
		context.stateGame.tier = tier;
	};"""
new = """	const setTier = (tier: 'basegame' | 'speed_dating' | 'after_dark') => {
		context.stateGame.gameType = tier === 'basegame' ? 'basegame' : 'freegame';
		context.stateGame.tier = tier;
		const musicName =
			tier === 'after_dark' ? 'bgm_after_dark' : tier === 'speed_dating' ? 'bgm_speed_dating' : 'bgm_main_louvo';
		context.eventEmitter.broadcast({ type: 'soundMusic', name: musicName });
	};"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : le panneau dev declenche maintenant aussi la bonne musique en changeant de palier.")
