results = []

# --- 1) sound.ts : ajouter les nouvelles cles, retirer les anciennes remplacees ---
path1 = "apps/louvo/src/game/sound.ts"
with open(path1, "r") as f:
    c1 = f.read()
old1 = """export type MusicName =
	| 'bgm_main'
	| 'bgm_freespin'
	| 'bgm_winlevel_big'"""
new1 = """export type MusicName =
	| 'bgm_main_louvo'
	| 'bgm_speed_dating'
	| 'bgm_after_dark'
	| 'bgm_winlevel_big'"""
count1 = c1.count(old1)
if count1 != 1:
    results.append(f"ERREUR sound.ts : trouve {count1} fois (attendu 1).")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK sound.ts : MusicName mis a jour (bgm_main_louvo/bgm_speed_dating/bgm_after_dark).")

# --- 2) assets.ts : enregistrer le nouveau sprite audio ---
path2 = "apps/louvo/src/game/assets.ts"
with open(path2, "r") as f:
    c2 = f.read()
old2 = """	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;"""
new2 = """	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
	louvoMusic: {
		type: 'audio',
		src: new URL('../../assets/audio/louvo_music.json', import.meta.url).href,
		preload: true,
	},
} as const;"""
count2 = c2.count(old2)
if count2 != 1:
    results.append(f"ERREUR assets.ts : trouve {count2} fois (attendu 1).")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK assets.ts : louvoMusic enregistre.")

# --- 3) bookEventHandlerMap.ts : logique tier-aware + remplacement bgm_main ---
path3 = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path3, "r") as f:
    c3 = f.read()

old3a = "const winLevelSoundsPlay = ({ winLevelData }: { winLevelData: WinLevelData }) => {"
new3a = """const freeSpinMusicName = () => (stateGame.tier === 'after_dark' ? 'bgm_after_dark' : 'bgm_speed_dating');

const winLevelSoundsPlay = ({ winLevelData }: { winLevelData: WinLevelData }) => {"""
count3a = c3.count(old3a)
if count3a != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts (helper) : trouve {count3a} fois (attendu 1).")
else:
    c3 = c3.replace(old3a, new3a, 1)
    results.append("OK bookEventHandlerMap.ts : freeSpinMusicName ajoutee.")

old3b = """	if (stateBet.activeBetModeKey === 'SUPERSPIN' || stateGame.gameType === 'freegame') {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
	} else {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main' });
	}"""
new3b = """	if (stateBet.activeBetModeKey === 'SUPERSPIN' || stateGame.gameType === 'freegame') {
		eventEmitter.broadcast({ type: 'soundMusic', name: freeSpinMusicName() });
	} else {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main_louvo' });
	}"""
count3b = c3.count(old3b)
if count3b != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts (winLevelSoundsStop) : trouve {count3b} fois (attendu 1).")
else:
    c3 = c3.replace(old3b, new3b, 1)
    results.append("OK bookEventHandlerMap.ts : winLevelSoundsStop tier-aware.")

old3c = "eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });"
count3c = c3.count(old3c)
if count3c != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts (freeSpinTrigger) : trouve {count3c} fois (attendu 1, celui de winLevelSoundsStop deja remplace).")
else:
    c3 = c3.replace(old3c, "eventEmitter.broadcast({ type: 'soundMusic', name: freeSpinMusicName() });", 1)
    results.append("OK bookEventHandlerMap.ts : freeSpinTrigger tier-aware.")

with open(path3, "w") as f:
    f.write(c3)

# --- 4) Sound.svelte : remplacements simples (bgm_main -> bgm_main_louvo, bgm_freespin -> bgm_speed_dating par defaut) ---
path4 = "apps/louvo/src/components/Sound.svelte"
with open(path4, "r") as f:
    c4 = f.read()
n_main = c4.count("'bgm_main'")
n_fs = c4.count("'bgm_freespin'")
c4 = c4.replace("'bgm_main'", "'bgm_main_louvo'")
c4 = c4.replace("'bgm_freespin'", "'bgm_speed_dating'")
with open(path4, "w") as f:
    f.write(c4)
results.append(f"OK Sound.svelte : {n_main} occurrence(s) bgm_main -> bgm_main_louvo, {n_fs} occurrence(s) bgm_freespin -> bgm_speed_dating (cas de bord, non tier-aware ici mais safe).")

for r in results:
    print(r)
