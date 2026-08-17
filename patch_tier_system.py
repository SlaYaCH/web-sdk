# --- typesBookEvent.ts : ajouter le champ tier (optionnel pour l'instant) ---
path = "apps/louvo/src/game/typesBookEvent.ts"
with open(path, "r") as f:
    content = f.read()

old_type = """type BookEventFreeSpinTrigger = {
	index: number;
	type: 'freeSpinTrigger';
	totalFs: number;
	positions: Position[];
};"""
new_type = """type BookEventFreeSpinTrigger = {
	index: number;
	type: 'freeSpinTrigger';
	totalFs: number;
	positions: Position[];
	tier?: 'speed_dating' | 'after_dark';
};"""

if old_type not in content:
    print("ERREUR typesBookEvent.ts : ancre introuvable.")
else:
    content = content.replace(old_type, new_type, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : typesBookEvent.ts a le champ tier (optionnel).")

# --- bookEventHandlerMap.ts : stocker/reinitialiser le tier ---
path = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path, "r") as f:
    content = f.read()

old_set = "stateGame.gameType = 'freegame';"
new_set = "stateGame.gameType = 'freegame';\n\t\tstateGame.tier = bookEvent.tier ?? 'speed_dating';"

old_reset = "stateGame.gameType = 'basegame';"
new_reset = "stateGame.gameType = 'basegame';\n\t\tstateGame.tier = 'basegame';"

missing = [n for n, o in [("set", old_set), ("reset", old_reset)] if o not in content]
if missing:
    print("ERREUR bookEventHandlerMap.ts : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_set, new_set, 1)
    content = content.replace(old_reset, new_reset, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bookEventHandlerMap.ts fixe/reinitialise le tier.")

# --- stateGame.svelte.ts : ajouter tier a l'etat global ---
path = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path, "r") as f:
    content = f.read()

old_state = """export const stateGame = $state({
	board,
	gameType: 'basegame' as GameType,
	multiplierBoard: [] as (MultiplierSymbol | undefined)[][],
	scatterCounter: 0,
});"""
new_state = """export const stateGame = $state({
	board,
	gameType: 'basegame' as GameType,
	tier: 'basegame' as 'basegame' | 'speed_dating' | 'after_dark',
	multiplierBoard: [] as (MultiplierSymbol | undefined)[][],
	scatterCounter: 0,
});"""

if old_state not in content:
    print("ERREUR stateGame.svelte.ts : ancre introuvable (fichier peut-etre modifie depuis - collez-le moi si besoin).")
else:
    content = content.replace(old_state, new_state, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : stateGame.svelte.ts a le champ tier.")

# --- Background.svelte : Speed Dating = fond jour, After Dark = fond nuit ---
path = "apps/louvo/src/components/Background.svelte"
with open(path, "r") as f:
    content = f.read()

old_derived = """	const showBaseBackground = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureBackground = $derived(context.stateGame.gameType === 'freegame');"""
new_derived = """	const showBaseBackground = $derived(
		context.stateGame.gameType === 'basegame' || context.stateGame.tier === 'speed_dating',
	);
	const showFeatureBackground = $derived(context.stateGame.tier === 'after_dark');"""

if old_derived not in content:
    print("ERREUR Background.svelte : ancre introuvable.")
else:
    content = content.replace(old_derived, new_derived, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Background.svelte distingue Speed Dating (jour) d'After Dark (nuit).")

# --- BoardFrame.svelte : meme logique pour le cadre ---
path = "apps/louvo/src/components/BoardFrame.svelte"
with open(path, "r") as f:
    content = f.read()

old_derived2 = """	const showBaseFrame = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureFrame = $derived(context.stateGame.gameType === 'freegame');"""
new_derived2 = """	const showBaseFrame = $derived(
		context.stateGame.gameType === 'basegame' || context.stateGame.tier === 'speed_dating',
	);
	const showFeatureFrame = $derived(context.stateGame.tier === 'after_dark');"""

if old_derived2 not in content:
    print("ERREUR BoardFrame.svelte : ancre introuvable.")
else:
    content = content.replace(old_derived2, new_derived2, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : BoardFrame.svelte distingue Speed Dating d'After Dark.")

# --- DevRevealPanel.svelte : boutons de test pour forcer le tier ---
path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

old_trigger_end = """		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
			likePositions,
		});
	};"""
new_trigger_end = old_trigger_end + """

	const setTier = (tier: 'basegame' | 'speed_dating' | 'after_dark') => {
		context.stateGame.gameType = tier === 'basegame' ? 'basegame' : 'freegame';
		context.stateGame.tier = tier;
	};"""

old_last_row = """		<div class="dev-panel__row">
			{#each Array.from({ length: REEL_COUNT }) as _, reelIndex}
				<button onclick={() => trigger(reelIndex)}>Rouleau {reelIndex + 1}</button>
			{/each}
		</div>
	</div>
{/if}"""
new_last_row = """		<div class="dev-panel__row">
			{#each Array.from({ length: REEL_COUNT }) as _, reelIndex}
				<button onclick={() => trigger(reelIndex)}>Rouleau {reelIndex + 1}</button>
			{/each}
		</div>
		<div class="dev-panel__row">
			<button onclick={() => setTier('basegame')}>Base</button>
			<button onclick={() => setTier('speed_dating')}>Speed Dating</button>
			<button onclick={() => setTier('after_dark')}>After Dark</button>
		</div>
	</div>
{/if}"""

missing2 = [n for n, o in [("trigger_end", old_trigger_end), ("last_row", old_last_row)] if o not in content]
if missing2:
    print("ERREUR DevRevealPanel.svelte : ancre(s) introuvable(s) :", missing2)
else:
    content = content.replace(old_trigger_end, new_trigger_end, 1)
    content = content.replace(old_last_row, new_last_row, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : panneau dev a 3 boutons pour forcer Base/Speed Dating/After Dark.")
