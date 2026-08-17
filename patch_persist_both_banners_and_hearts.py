results = []

# --- 1) SpecialRevealOverlay.svelte : maintien indefini pour LES DEUX types ---
path1 = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1 = "holdMs={6000}"
count1 = c1.count(old1)
if count1 != 1:
    results.append(f"ERREUR SpecialRevealOverlay.svelte (holdMs) : trouve {count1} fois (attendu 1).")
else:
    new1 = "holdMs={Infinity}"
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK SpecialRevealOverlay.svelte : maintien infini pour MATCH et SUPER LIKE (fermeture uniquement au prochain spin).")

# --- 2) SuperlikeHeartThrow.svelte : les coeurs restent visibles apres atterrissage (pas de fondu) ---
path2 = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					resolve();
					fadeOut(index);
				}"""
new2 = """				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					resolve();
					// Reste visible (pas de fondu) jusqu'au prochain spin,
					// comme la banniere qui l'accompagne.
				}"""

count2 = c2.count(old2)
if count2 != 1:
    results.append(f"ERREUR SuperlikeHeartThrow.svelte : trouve {count2} fois (attendu 1).")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK SuperlikeHeartThrow.svelte : coeurs restent visibles apres atterrissage (plus de fondu automatique).")

# --- 3) bookEventHandlerMap.ts : matchDuelReveal ET superlikeReveal ne bloquent plus la suite ---
path3 = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path3, "r") as f:
    c3 = f.read()

old3a = """	matchDuelReveal: async (bookEvent: BookEventOfType<'matchDuelReveal'>) => {
		await eventEmitter.broadcastAsync({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'M',
			multiplier: bookEvent.multiplier,
			duelValues: bookEvent.duelValues,
		});
	},"""
new3a = """	matchDuelReveal: async (bookEvent: BookEventOfType<'matchDuelReveal'>) => {
		// Ne bloque plus la suite de la sequence : la banniere reste affichee
		// indefiniment (voir SpecialRevealOverlay) et se fermera uniquement au
		// prochain spin (spinStart -> forceClose), pas sur un minuteur.
		eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'M',
			multiplier: bookEvent.multiplier,
			duelValues: bookEvent.duelValues,
		});
	},"""
count3a = c3.count(old3a)
if count3a != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts (matchDuelReveal) : trouve {count3a} fois (attendu 1).")
else:
    c3 = c3.replace(old3a, new3a, 1)
    results.append("OK bookEventHandlerMap.ts : matchDuelReveal ne bloque plus la sequence.")

old3b = """	superlikeReveal: async (bookEvent: BookEventOfType<'superlikeReveal'>) => {
		await eventEmitter.broadcastAsync({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'K',
			multiplier: bookEvent.multiplier,
			likePositions: bookEvent.likePositions,
		});
		stateGame.streakTier = bookEvent.streakTier;
		stateGame.streakLikes = bookEvent.likes;
	},"""
new3b = """	superlikeReveal: async (bookEvent: BookEventOfType<'superlikeReveal'>) => {
		// Ne bloque plus la suite de la sequence, meme raison que matchDuelReveal.
		eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'K',
			multiplier: bookEvent.multiplier,
			likePositions: bookEvent.likePositions,
		});
		stateGame.streakTier = bookEvent.streakTier;
		stateGame.streakLikes = bookEvent.likes;
	},"""
count3b = c3.count(old3b)
if count3b != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts (superlikeReveal) : trouve {count3b} fois (attendu 1).")
else:
    c3 = c3.replace(old3b, new3b, 1)
    results.append("OK bookEventHandlerMap.ts : superlikeReveal ne bloque plus la sequence.")

with open(path3, "w") as f:
    f.write(c3)

for r in results:
    print(r)
