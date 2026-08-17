path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

old_trigger = """	const trigger = (reelIndex: number) => {
		const likePositions =
			symbol === 'K'
				? Array.from({ length: likesCount }, () => ({
						reelIndex: Math.floor(Math.random() * REEL_COUNT),
						rowIndex: Math.floor(Math.random() * REEL_COUNT),
					}))
				: undefined;

		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
			likePositions,
		});
	};"""

new_trigger = """	const trigger = (reelIndex: number) => {
		// Reproduit fidelement la vraie logique _fire_likes du Math SDK :
		// jamais de doublon, jamais sur la colonne deja wild de la banniere.
		let likePositions: { reelIndex: number; rowIndex: number }[] | undefined;
		if (symbol === 'K') {
			const candidates: { reelIndex: number; rowIndex: number }[] = [];
			for (let r = 0; r < REEL_COUNT; r++) {
				if (r === reelIndex) continue;
				for (let row = 0; row < REEL_COUNT; row++) {
					candidates.push({ reelIndex: r, rowIndex: row });
				}
			}
			for (let i = candidates.length - 1; i > 0; i--) {
				const j = Math.floor(Math.random() * (i + 1));
				[candidates[i], candidates[j]] = [candidates[j], candidates[i]];
			}
			likePositions = candidates.slice(0, likesCount);
		}

		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
			likePositions,
		});
	};"""

if old_trigger not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old_trigger, new_trigger, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : panneau dev tire des positions uniques, jamais sur la colonne de la banniere.")
