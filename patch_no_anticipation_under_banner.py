results = []

# --- 1) stateGame.svelte.ts : nouveau champ ---
path1 = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path1, "r") as f:
    c1 = f.read()

old1 = "\tstreakTier: 0,\n\tstreakLikes: 0,\n});"
new1 = "\tstreakTier: 0,\n\tstreakLikes: 0,\n\tactiveBannerReelIndex: null as number | null,\n});"
n = c1.count(old1)
if n != 1:
    results.append(f"ERREUR (stateGame) : {n} fois.")
else:
    c1 = c1.replace(old1, new1, 1)
    results.append("OK (champ activeBannerReelIndex ajoute)")
with open(path1, "w") as f:
    f.write(c1)

# --- 2) SpecialRevealOverlay.svelte : maj du champ a l'ouverture/fermeture ---
path2 = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2a = "\t\t\trevealId += 1;\n\t\t\tshow = true;"
new2a = "\t\t\trevealId += 1;\n\t\t\tshow = true;\n\t\t\tcontext.stateGame.activeBannerReelIndex = emitterEvent.reelIndex;"
n = c2.count(old2a)
if n != 1:
    results.append(f"ERREUR (ouverture) : {n} fois.")
else:
    c2 = c2.replace(old2a, new2a, 1)
    results.append("OK (activeBannerReelIndex mis a jour a l'ouverture)")

old2b = "\t\t\tawait waitForResolve((resolve) => (resolveShow = resolve));\n\t\t\tshow = false;"
new2b = "\t\t\tawait waitForResolve((resolve) => (resolveShow = resolve));\n\t\t\tshow = false;\n\t\t\tcontext.stateGame.activeBannerReelIndex = null;"
n = c2.count(old2b)
if n != 1:
    results.append(f"ERREUR (fermeture) : {n} fois.")
else:
    c2 = c2.replace(old2b, new2b, 1)
    results.append("OK (activeBannerReelIndex remis a null a la fermeture)")
with open(path2, "w") as f:
    f.write(c2)

# --- 3) Anticipations.svelte : ne pas declencher sur la colonne occupee ---
path3 = "apps/louvo/src/components/Anticipations.svelte"
with open(path3, "r") as f:
    c3 = f.read()

old3a = """	const hasAnticipation = $derived(
		context.stateGame.board.some((reel) => reel.reelState.anticipating),
	);"""
new3a = """	// Un DATE ne doit jamais declencher/rester en anticipation sur la
	// colonne ou une banniere (Super Like/Match Duel) est deja affichee.
	const hasAnticipation = $derived(
		context.stateGame.board.some(
			(reel) =>
				reel.reelState.anticipating && reel.reelIndex !== context.stateGame.activeBannerReelIndex,
		),
	);"""
n = c3.count(old3a)
if n != 1:
    results.append(f"ERREUR (hasAnticipation) : {n} fois.")
else:
    c3 = c3.replace(old3a, new3a, 1)
    results.append("OK (hasAnticipation exclut la colonne occupee)")

old3b = """{#each context.stateGame.board as reel}
	{#if reel.reelState.anticipating}
		<Anticipation {reel} oncomplete={() => (reel.reelState.anticipating = false)} />
	{/if}
{/each}"""
new3b = """{#each context.stateGame.board as reel}
	{#if reel.reelState.anticipating && reel.reelIndex !== context.stateGame.activeBannerReelIndex}
		<Anticipation {reel} oncomplete={() => (reel.reelState.anticipating = false)} />
	{/if}
{/each}"""
n = c3.count(old3b)
if n != 1:
    results.append(f"ERREUR (each) : {n} fois.")
else:
    c3 = c3.replace(old3b, new3b, 1)
    results.append("OK (rendu exclut aussi la colonne occupee)")
with open(path3, "w") as f:
    f.write(c3)

for r in results:
    print(r)
