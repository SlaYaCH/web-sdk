# --- BannerReveal.svelte ---
path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import MatchDuelClash from './MatchDuelClash.svelte';"
new_import = old_import + "\n\timport SuperlikeBarilletDisplay from './SuperlikeBarilletDisplay.svelte';"

old_props = """	type Props = {
		assetKey: string;
		multiplierText?: string;
		duelValues?: [number, number];
		duelWinner?: number;
		forceClose?: boolean;
		x?: number;
		y?: number;
		durationInMs?: number;
		holdMs?: number;
		zIndex?: number;
		oncomplete?: () => void;
	};"""
new_props = """	type Props = {
		assetKey: string;
		multiplierText?: string;
		duelValues?: [number, number];
		duelWinner?: number;
		likes?: number;
		forceClose?: boolean;
		x?: number;
		y?: number;
		durationInMs?: number;
		holdMs?: number;
		zIndex?: number;
		oncomplete?: () => void;
	};"""

old_block = """	{#if props.assetKey === 'matchReveal' && props.duelValues && props.duelWinner !== undefined}
		<MatchDuelClash duelValues={props.duelValues} winner={props.duelWinner} />
	{:else if props.multiplierText}
		<BitmapText
			anchor={0.5}
			y={0}
			text={props.multiplierText}
			style={{
				fontFamily: 'gold',
				fontSize: 60,
			}}
		/>
	{/if}"""
new_block = old_block + """

	{#if props.assetKey === 'superlikeReveal' && props.likes}
		<SuperlikeBarilletDisplay likes={props.likes} />
	{/if}"""

missing = [n for n, o in [("import", old_import), ("props", old_props), ("block", old_block)] if o not in content]
if missing:
    print("ERREUR BannerReveal.svelte : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_props, new_props, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : BannerReveal.svelte affiche le presentoir a coeurs.")

# --- SpecialRevealOverlay.svelte ---
path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_state = "let likePositions = $state<{ reelIndex: number; rowIndex: number }[] | undefined>(undefined);"
new_state = old_state + "\n\tlet likes = $state(0);"

old_handler = "likePositions = emitterEvent.likePositions;"
new_handler = old_handler + "\n\t\t\tlikes = emitterEvent.likePositions?.length ?? 0;"

old_banner = """				duelValues={duelValues}
				duelWinner={multiplier}"""
new_banner = old_banner + "\n\t\t\t\tlikes={likes}"

missing2 = [n for n, o in [("state", old_state), ("handler", old_handler), ("banner", old_banner)] if o not in content]
if missing2:
    print("ERREUR SpecialRevealOverlay.svelte : ancre(s) non trouvee(s) :", missing2)
else:
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_handler, new_handler, 1)
    content = content.replace(old_banner, new_banner, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SpecialRevealOverlay.svelte transmet likes au presentoir.")

# --- DevRevealPanel.svelte ---
path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

old_state2 = "let secondDuelValue = $state(3);"
new_state2 = old_state2 + "\n\tlet likesCount = $state(3);"

old_trigger = """	const trigger = (reelIndex: number) => {
		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
		});
	};"""
new_trigger = """	const trigger = (reelIndex: number) => {
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

old_label = """			{#if symbol === 'M'}
				<label>
					vs x
					<input type="number" min="1" max="50" bind:value={secondDuelValue} />
				</label>
			{/if}"""
new_label = old_label + """
			{#if symbol === 'K'}
				<label>
					likes
					<input type="number" min="1" max="6" bind:value={likesCount} />
				</label>
			{/if}"""

missing3 = [n for n, o in [("state2", old_state2), ("trigger", old_trigger), ("label", old_label)] if o not in content]
if missing3:
    print("ERREUR DevRevealPanel.svelte : ancre(s) non trouvee(s) :", missing3)
else:
    content = content.replace(old_state2, new_state2, 1)
    content = content.replace(old_trigger, new_trigger, 1)
    content = content.replace(old_label, new_label, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : DevRevealPanel.svelte a un champ 'likes' pour tester le presentoir.")
