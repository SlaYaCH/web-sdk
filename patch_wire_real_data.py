# --- typesBookEvent.ts : ajouter les champs manquants aux vrais events ---
path = "apps/louvo/src/game/typesBookEvent.ts"
with open(path, "r") as f:
    content = f.read()

old_match = """type BookEventMatchDuelReveal = {
	index: number;
	type: 'matchDuelReveal';
	reelIndex: number;
	multiplier: number;
};"""
new_match = """type BookEventMatchDuelReveal = {
	index: number;
	type: 'matchDuelReveal';
	reelIndex: number;
	multiplier: number;
	duelValues: [number, number];
};"""

old_superlike = """type BookEventSuperlikeReveal = {
	index: number;
	type: 'superlikeReveal';
	reelIndex: number;
	multiplier: number;
	likes: number;
};"""
new_superlike = """type BookEventSuperlikeReveal = {
	index: number;
	type: 'superlikeReveal';
	reelIndex: number;
	multiplier: number;
	likes: number;
	likePositions: { reelIndex: number; rowIndex: number }[];
};"""

missing = [n for n, o in [("match", old_match), ("superlike", old_superlike)] if o not in content]
if missing:
    print("ERREUR typesBookEvent.ts : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_match, new_match, 1)
    content = content.replace(old_superlike, new_superlike, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : typesBookEvent.ts a jour avec duelValues/likePositions.")

# --- bookEventHandlerMap.ts : transmettre les vraies donnees ---
path = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path, "r") as f:
    content = f.read()

old_match_handler = """	matchDuelReveal: async (bookEvent: BookEventOfType<'matchDuelReveal'>) => {
		await eventEmitter.broadcastAsync({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'M',
			multiplier: bookEvent.multiplier,
		});
	},"""
new_match_handler = """	matchDuelReveal: async (bookEvent: BookEventOfType<'matchDuelReveal'>) => {
		await eventEmitter.broadcastAsync({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'M',
			multiplier: bookEvent.multiplier,
			duelValues: bookEvent.duelValues,
		});
	},"""

old_superlike_handler = """	superlikeReveal: async (bookEvent: BookEventOfType<'superlikeReveal'>) => {
		await eventEmitter.broadcastAsync({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'K',
			multiplier: bookEvent.multiplier,
		});
	},"""
new_superlike_handler = """	superlikeReveal: async (bookEvent: BookEventOfType<'superlikeReveal'>) => {
		await eventEmitter.broadcastAsync({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'K',
			multiplier: bookEvent.multiplier,
			likePositions: bookEvent.likePositions,
		});
	},"""

missing2 = [n for n, o in [("match_handler", old_match_handler), ("superlike_handler", old_superlike_handler)] if o not in content]
if missing2:
    print("ERREUR bookEventHandlerMap.ts : ancre(s) non trouvee(s) :", missing2)
else:
    content = content.replace(old_match_handler, new_match_handler, 1)
    content = content.replace(old_superlike_handler, new_superlike_handler, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bookEventHandlerMap.ts transmet duelValues/likePositions.")

# --- SpecialRevealOverlay.svelte : stocker et transmettre likePositions ---
path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_type = """	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
		duelValues?: [number, number];
	};"""
new_type = """	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
		duelValues?: [number, number];
		likePositions?: { reelIndex: number; rowIndex: number }[];
	};"""

old_state = "let duelValues = $state<[number, number] | undefined>(undefined);"
new_state = old_state + "\n\tlet likePositions = $state<{ reelIndex: number; rowIndex: number }[] | undefined>(undefined);"

old_handler = "duelValues = emitterEvent.duelValues;"
new_handler = old_handler + "\n\t\t\tlikePositions = emitterEvent.likePositions;"

old_heartthrow = "<SuperlikeHeartThrow reelIndex={revealReelIndex} />"
new_heartthrow = "<SuperlikeHeartThrow reelIndex={revealReelIndex} positions={likePositions} />"

missing3 = [n for n, o in [("type", old_type), ("state", old_state), ("handler", old_handler), ("heartthrow", old_heartthrow)] if o not in content]
if missing3:
    print("ERREUR SpecialRevealOverlay.svelte : ancre(s) non trouvee(s) :", missing3)
else:
    content = content.replace(old_type, new_type, 1)
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_handler, new_handler, 1)
    content = content.replace(old_heartthrow, new_heartthrow, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SpecialRevealOverlay.svelte transmet likePositions au lancer de coeurs.")
