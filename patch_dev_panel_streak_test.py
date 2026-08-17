path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "let likesCount = $state(3);"
new1 = "let likesCount = $state(3);\n\tlet streakTierTest = $state(0);"
if old1 not in content:
    results.append("ERREUR (state) : ancre introuvable.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (state) : streakTierTest ajoute.")

old2 = """context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
			likePositions,
		});
	};"""
new2 = """context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
			likePositions,
		});
		if (symbol === 'K') {
			context.stateGame.streakTier = streakTierTest;
			context.stateGame.streakLikes = likesCount;
		}
	};"""
if old2 not in content:
    results.append("ERREUR (trigger) : ancre introuvable.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (trigger) : mise a jour du streak ajoutee au declenchement SUPER LIKE.")

old3 = """\t\t\t{#if symbol === 'K'}
				<label>
					likes
					<input type="number" min="1" max="6" bind:value={likesCount} />
				</label>
			{/if}"""
new3 = """\t\t\t{#if symbol === 'K'}
				<label>
					likes
					<input type="number" min="1" max="6" bind:value={likesCount} />
				</label>
				<label>
					streak (0-4)
					<input type="number" min="0" max="4" bind:value={streakTierTest} />
				</label>
			{/if}"""
if old3 not in content:
    results.append("ERREUR (UI) : ancre introuvable.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (UI) : champ streak (0-4) ajoute a cote de likes.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
