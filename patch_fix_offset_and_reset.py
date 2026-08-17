results = []

# --- 1) Game.svelte : corriger le decalage (streakTier = index DIRECT du palier actif, 1 a 4) ---
path1 = "apps/louvo/src/components/Game.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1 = """\t\t\t\t<AfterDarkStreakDisplay
					tier2={{
						filled: context.stateGame.streakTier === 0 ? 6 - context.stateGame.streakLikes : 0,
						achieved: context.stateGame.streakTier >= 1,
					}}
					tier3={{
						filled:
							context.stateGame.streakTier === 1
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 1
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 2,
					}}
					tier4={{
						filled:
							context.stateGame.streakTier === 2
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 2
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 3,
					}}
					tier5x={{
						filled:
							context.stateGame.streakTier === 3
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 3
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 4,
					}}
				/>"""

new1 = """\t\t\t\t<AfterDarkStreakDisplay
					tier2={{
						filled:
							context.stateGame.streakTier === 1
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier >= 2
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 2,
					}}
					tier3={{
						filled:
							context.stateGame.streakTier === 2
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier >= 3
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 3,
					}}
					tier4={{
						filled:
							context.stateGame.streakTier === 3
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier >= 4
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 4,
					}}
					tier5x={{
						filled:
							context.stateGame.streakTier === 4
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 4
									? 0
									: 6,
						achieved: context.stateGame.streakTier > 4,
					}}
				/>"""

count1 = c1.count(old1)
if count1 != 1:
    results.append(f"ERREUR Game.svelte : trouve {count1} fois (attendu 1).")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK Game.svelte : decalage corrige (streakTier = palier actif direct, 1 a 4).")

# --- 2) DevRevealPanel.svelte : bouton reset pour tester proprement ---
path2 = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """<button onclick={() => setTier('after_dark')}>After Dark</button>
		</div>"""
new2 = """<button onclick={() => setTier('after_dark')}>After Dark</button>
		</div>
		<div class="dev-panel__row">
			<button
				onclick={() => {
					context.stateGame.streakTier = 0;
					context.stateGame.streakLikes = 0;
				}}
			>
				Reset streak
			</button>
		</div>"""
count2 = c2.count(old2)
if count2 != 1:
    results.append(f"ERREUR DevRevealPanel.svelte : trouve {count2} fois (attendu 1).")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK DevRevealPanel.svelte : bouton Reset streak ajoute.")

for r in results:
    print(r)
