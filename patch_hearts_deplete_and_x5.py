path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

# --- 1) Inverser la logique : coeurs RESTANTS (6 - likes) au lieu de coeurs AJOUTES ---
replacements = [
    (
        "filled: context.stateGame.streakTier === 0 ? context.stateGame.streakLikes : 6,",
        "filled: context.stateGame.streakTier === 0 ? 6 - context.stateGame.streakLikes : 0,",
    ),
    (
        """filled:
							context.stateGame.streakTier === 1
								? context.stateGame.streakLikes
								: context.stateGame.streakTier > 1
									? 6
									: 0,""",
        """filled:
							context.stateGame.streakTier === 1
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 1
									? 0
									: 6,""",
    ),
    (
        """filled:
							context.stateGame.streakTier === 2
								? context.stateGame.streakLikes
								: context.stateGame.streakTier > 2
									? 6
									: 0,""",
        """filled:
							context.stateGame.streakTier === 2
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 2
									? 0
									: 6,""",
    ),
    (
        """filled: {
						context.stateGame.streakTier === 3
							? context.stateGame.streakLikes
							: context.stateGame.streakTier > 3
								? 6
								: 0
					}""".replace("filled: {", "filled:").replace("}", "", 1),
        None,  # place holder, handled separately below (tier5x has different bracket style)
    ),
]

for old, new in replacements:
    if new is None:
        continue
    count = content.count(old)
    if count != 1:
        results.append(f"ERREUR : ancre non trouvee une seule fois (trouve {count}) pour un bloc filled.")
    else:
        content = content.replace(old, new, 1)
        results.append("OK : un bloc filled inverse (coeurs restants).")

# tier5x a une syntaxe {  } differente (avec accolades sur plusieurs lignes) - traite a part
old_5x = """filled={
						context.stateGame.streakTier === 3
							? context.stateGame.streakLikes
							: context.stateGame.streakTier > 3
								? 6
								: 0
					}
					duelCardKey="duel5x\""""
new_5x = """filled={
						context.stateGame.streakTier === 3
							? 6 - context.stateGame.streakLikes
							: context.stateGame.streakTier > 3
								? 0
								: 6
					}
					duelCardKey="duel5x"
					duelAchieved={context.stateGame.streakTier >= 4}"""

count5x = content.count(old_5x)
if count5x != 1:
    results.append(f"ERREUR tier5x : ancre introuvable (trouve {count5x} fois).")
else:
    content = content.replace(old_5x, new_5x, 1)
    results.append("OK tier5x : coeurs inverses + duelAchieved ajoute.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
