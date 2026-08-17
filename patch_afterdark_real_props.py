path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = """<AfterDarkStreakDisplay
					tier2={{ filled: 6, achieved: true }}
					tier3={{ filled: 3, achieved: false }}
					tier4={{ filled: 0, achieved: false }}
					tier5x={{ filled: 2, achieved: false }}
				/>"""

new = """<AfterDarkStreakDisplay
					tier2={{
						filled: context.stateGame.streakTier === 0 ? context.stateGame.streakLikes : 6,
						achieved: context.stateGame.streakTier >= 1,
					}}
					tier3={{
						filled:
							context.stateGame.streakTier === 1
								? context.stateGame.streakLikes
								: context.stateGame.streakTier > 1
									? 6
									: 0,
						achieved: context.stateGame.streakTier >= 2,
					}}
					tier4={{
						filled:
							context.stateGame.streakTier === 2
								? context.stateGame.streakLikes
								: context.stateGame.streakTier > 2
									? 6
									: 0,
						achieved: context.stateGame.streakTier >= 3,
					}}
					tier5x={{
						filled:
							context.stateGame.streakTier === 3
								? context.stateGame.streakLikes
								: context.stateGame.streakTier > 3
									? 6
									: 0,
						achieved: context.stateGame.streakTier >= 4,
					}}
				/>"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : bloc de test introuvable tel quel (trouve {count} fois, attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : AfterDarkStreakDisplay branche sur les vraies donnees streakTier/streakLikes.")
