results = []

# --- 1) Game.svelte : inverser filled pour tier5x uniquement ---
path1 = "apps/louvo/src/components/Game.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1 = """\t\t\t\t\ttier5x={{
						filled:
							context.stateGame.streakTier === 3
								? context.stateGame.streakLikes
								: context.stateGame.streakTier > 3
									? 6
									: 0,
						achieved: context.stateGame.streakTier >= 4,
					}}"""
new1 = """\t\t\t\t\ttier5x={{
						filled:
							context.stateGame.streakTier === 3
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 3
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 4,
					}}"""
count1 = c1.count(old1)
if count1 != 1:
    results.append(f"ERREUR Game.svelte : trouve {count1} fois (attendu 1).")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK Game.svelte : filled inverse pour tier5x.")

# --- 2) AfterDarkStreakDisplay.svelte : transmettre achieved au groupe DUEL X5 ---
path2 = "apps/louvo/src/components/AfterDarkStreakDisplay.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """<AfterDarkStreakGroup
			filled={t5x().filled}
			duelCardKey="duel5x\""""
new2 = """<AfterDarkStreakGroup
			filled={t5x().filled}
			duelCardKey="duel5x"
			duelAchieved={t5x().achieved}"""
count2 = c2.count(old2)
if count2 != 1:
    results.append(f"ERREUR AfterDarkStreakDisplay.svelte : trouve {count2} fois (attendu 1).")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK AfterDarkStreakDisplay.svelte : duelAchieved transmis pour le groupe X5.")

for r in results:
    print(r)
