# --- game/utils.ts : signaler le debut de chaque spin ---
path = "apps/louvo/src/game/utils.ts"
with open(path, "r") as f:
    content = f.read()

old_playbet = """export const playBet = async (bet: Bet) => {
	stateBet.winBookEventAmount = 0;
	await playBookEvents(bet.state);
	eventEmitter.broadcast({ type: 'stopButtonEnable' });
};"""
new_playbet = """export const playBet = async (bet: Bet) => {
	// Signale qu'un nouveau spin demarre - permet a une UI encore ouverte
	// (ex: banniere de reveal du spin precedent) de se refermer d'elle-meme
	// au lieu de dependre d'un minuteur arbitraire.
	eventEmitter.broadcast({ type: 'spinStart' });
	stateBet.winBookEventAmount = 0;
	await playBookEvents(bet.state);
	eventEmitter.broadcast({ type: 'stopButtonEnable' });
};"""

if old_playbet not in content:
    print("ERREUR utils.ts : ancre introuvable.")
else:
    content = content.replace(old_playbet, new_playbet, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : utils.ts emet spinStart au debut de chaque spin.")

# --- BannerReveal.svelte : accepter une fermeture forcee externe ---
path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old_props = """	type Props = {
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
new_props = """	type Props = {
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

old_onmount = """	onMount(() => {
		(async () => {
			await animateTo(1, 1, durationInMs);

			if (holdMs > 0) {
				await new Promise((r) => setTimeout(r, holdMs));
				await animateTo(1, 0, Math.min(durationInMs, 250));
			}

			props.oncomplete?.();
		})();
	});"""
new_onmount = """	let resolveHold = () => {};

	onMount(() => {
		(async () => {
			await animateTo(1, 1, durationInMs);

			if (holdMs > 0) {
				await Promise.race([
					new Promise<void>((r) => setTimeout(r, holdMs)),
					new Promise<void>((r) => (resolveHold = r)),
				]);
				await animateTo(1, 0, Math.min(durationInMs, 250));
			}

			props.oncomplete?.();
		})();
	});

	$effect(() => {
		if (props.forceClose) resolveHold();
	});"""

missing = [n for n, o in [("props", old_props), ("onmount", old_onmount)] if o not in content]
if missing:
    print("ERREUR BannerReveal.svelte : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_props, new_props, 1)
    content = content.replace(old_onmount, new_onmount, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : BannerReveal.svelte accepte forceClose.")

# --- SpecialRevealOverlay.svelte : fermer sur spinStart, pas sur un timer ---
path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_state = "let bannerX = $state(0);"
new_state = "let bannerX = $state(0);\n\tlet forceClose = $state(false);"

old_subscribe_open = """	context.eventEmitter.subscribeOnMount({
		specialRevealShow: async (emitterEvent) => {"""
new_subscribe_open = """	context.eventEmitter.subscribeOnMount({
		spinStart: () => {
			if (show) forceClose = true;
		},
		specialRevealShow: async (emitterEvent) => {
			forceClose = false;"""

old_holdms = "holdMs={2200}"
new_holdms = "holdMs={15000}\n\t\t\t\tforceClose={forceClose}"

missing = [n for n, o in [("state", old_state), ("subscribe_open", old_subscribe_open), ("holdms", old_holdms)] if o not in content]
if missing:
    print("ERREUR SpecialRevealOverlay.svelte : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_subscribe_open, new_subscribe_open, 1)
    content = content.replace(old_holdms, new_holdms, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SpecialRevealOverlay.svelte se ferme sur spinStart (15s de securite max).")
