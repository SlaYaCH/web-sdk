# --- BannerReveal.svelte ---
path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { Container, Sprite, BitmapText } from 'pixi-svelte';"
new_import = old_import + "\n\timport MatchDuelClash from './MatchDuelClash.svelte';"

old_props = """	type Props = {
		assetKey: string;
		multiplierText?: string;
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
		x?: number;
		y?: number;
		durationInMs?: number;
		holdMs?: number;
		zIndex?: number;
		oncomplete?: () => void;
	};"""

old_text_block = """	{#if props.multiplierText}
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
new_text_block = """	{#if props.assetKey === 'matchReveal' && props.duelValues && props.duelWinner !== undefined}
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

missing = [n for n, o in [("import", old_import), ("props", old_props), ("text_block", old_text_block)] if o not in content]
if missing:
    print("ERREUR BannerReveal.svelte : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_props, new_props, 1)
    content = content.replace(old_text_block, new_text_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : BannerReveal.svelte branche sur MatchDuelClash.")

# --- SpecialRevealOverlay.svelte ---
path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_type = """	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
	};"""
new_type = """	export type EmitterEventSpecialReveal = {
		type: 'specialRevealShow';
		reelIndex: number;
		symbol: 'M' | 'K';
		multiplier: number;
		duelValues?: [number, number];
	};"""

old_state = "let multiplierText = $state('');"
new_state = "let multiplierText = $state('');\n\tlet multiplier = $state(0);\n\tlet duelValues = $state<[number, number] | undefined>(undefined);"

old_handler = "multiplierText = `x${emitterEvent.multiplier}`;"
new_handler = old_handler + "\n\t\t\tmultiplier = emitterEvent.multiplier;\n\t\t\tduelValues = emitterEvent.duelValues;"

old_banner_open = """			<BannerReveal
				{assetKey}
				{multiplierText}
				x={bannerX}"""
new_banner_open = """			<BannerReveal
				{assetKey}
				{multiplierText}
				duelValues={duelValues}
				duelWinner={multiplier}
				x={bannerX}"""

missing = [n for n, o in [("type", old_type), ("state", old_state), ("handler", old_handler), ("banner_open", old_banner_open)] if o not in content]
if missing:
    print("ERREUR SpecialRevealOverlay.svelte : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_type, new_type, 1)
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_handler, new_handler, 1)
    content = content.replace(old_banner_open, new_banner_open, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SpecialRevealOverlay.svelte transmet duelValues/duelWinner.")

# --- DevRevealPanel.svelte ---
path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

old_state2 = "let multiplier = $state(7);"
new_state2 = "let multiplier = $state(7);\n\tlet secondDuelValue = $state(3);"

old_trigger = """	const trigger = (reelIndex: number) => {
		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
		});
	};"""
new_trigger = """	const trigger = (reelIndex: number) => {
		context.eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex,
			symbol,
			multiplier,
			duelValues: symbol === 'M' ? [multiplier, secondDuelValue] : undefined,
		});
	};"""

old_label = """			<label>
				x
				<input type="number" min="1" max="50" bind:value={multiplier} />
			</label>"""
new_label = """			<label>
				x
				<input type="number" min="1" max="50" bind:value={multiplier} />
			</label>
			{#if symbol === 'M'}
				<label>
					vs x
					<input type="number" min="1" max="50" bind:value={secondDuelValue} />
				</label>
			{/if}"""

missing = [n for n, o in [("state2", old_state2), ("trigger", old_trigger), ("label", old_label)] if o not in content]
if missing:
    print("ERREUR DevRevealPanel.svelte : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_state2, new_state2, 1)
    content = content.replace(old_trigger, new_trigger, 1)
    content = content.replace(old_label, new_label, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : DevRevealPanel.svelte a maintenant un champ 'vs x' pour tester le duel.")
