# --- assets.ts : enregistrer les 2 paquets d'animation ---
path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;"""
new = """	matchRevealKiss: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/match-reveal/match_reveal_sharpstop_mobile.json', import.meta.url)
			.href,
	},
	matchRevealExit: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/match-exit/match_exit_final_locked_mobile.json', import.meta.url)
			.href,
	},

	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;"""

if old not in content:
    print("ERREUR assets.ts : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : matchRevealKiss/matchRevealExit enregistres dans assets.ts.")

# --- BannerReveal.svelte : basculer sur l'animation une fois le duel resolu ---
path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import SuperlikeBarilletDisplay from './SuperlikeBarilletDisplay.svelte';"
new_import = old_import + "\n\timport MatchOutcomeAnimation from './MatchOutcomeAnimation.svelte';"

old_state = "let scale = $state(0.6);"
new_state = """let duelResolved = $state(false);
	const biggerWon = $derived(
		props.duelValues && props.duelWinner !== undefined
			? props.duelWinner === Math.max(props.duelValues[0], props.duelValues[1])
			: true,
	);

	let scale = $state(0.6);"""

old_block = """	<Sprite anchor={0.5} key={props.assetKey} width={bannerWidth} height={bannerHeight} />

	{#if props.assetKey === 'matchReveal' && props.duelValues && props.duelWinner !== undefined}
		<MatchDuelClash duelValues={props.duelValues} winner={props.duelWinner} />
	{:else if props.multiplierText}"""
new_block = """	{#if props.assetKey === 'matchReveal' && duelResolved}
		<MatchOutcomeAnimation {biggerWon} width={bannerWidth} height={bannerHeight} />
	{:else}
		<Sprite anchor={0.5} key={props.assetKey} width={bannerWidth} height={bannerHeight} />
	{/if}

	{#if props.assetKey === 'matchReveal' && props.duelValues && props.duelWinner !== undefined}
		<MatchDuelClash
			duelValues={props.duelValues}
			winner={props.duelWinner}
			oncomplete={() => (duelResolved = true)}
		/>
	{:else if props.multiplierText}"""

missing = [n for n, o in [("import", old_import), ("state", old_state), ("block", old_block)] if o not in content]
if missing:
    print("ERREUR BannerReveal.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : BannerReveal.svelte bascule sur l'animation une fois le duel resolu.")

# --- SpecialRevealOverlay.svelte : plus de temps d'affichage pour laisser l'animation se jouer ---
path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_holdms = "holdMs={2500}"
new_holdms = "holdMs={5500}"

if old_holdms not in content:
    print("ERREUR SpecialRevealOverlay.svelte : ancre introuvable.")
else:
    content = content.replace(old_holdms, new_holdms, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : temps d'affichage porte a 5.5s (laisse la place a l'animation complete + au lancer sequentiel des coeurs).")
