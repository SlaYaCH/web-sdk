path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "	import { ButtonBetProvider } from 'components-ui-pixi';\n"
new_import = ""

old_logic_anchor = """	const onAutoSpin = () => {
		if (autoSpinDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (hasAutoBetCounter) {
			stateBet.autoSpinsCounter = 0;
		} else {
			stateModal.modal = { name: 'autoSpin' };
		}
	};"""
new_logic_anchor = old_logic_anchor + """

	// --- Spin / Stop (logique reprise directement de ButtonBetProvider.svelte,
	// qui n'est pas exporte publiquement par components-ui-pixi) ---
	let stopDisabled = $state(false);
	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => (stopDisabled = true),
		stopButtonEnable: () => (stopDisabled = false),
	});
	const spinDisabled = $derived.by(() => {
		if (context.stateXstateDerived.isIdle()) {
			return !stateBetDerived.isBetCostAvailable();
		}
		if (stopDisabled) return true;
		if (!stateBetDerived.hasAutoBetCounter() && stateBet.isTurbo) return true;
		return false;
	});
	const onSpinPress = () => {
		context.eventEmitter.broadcast({ type: 'soundPressBet' });
		if (context.stateXstateDerived.isIdle()) {
			if (stateBetDerived.activeBetMode()?.type === 'buy') stateBet.activeBetModeKey = 'BASE';
			context.eventEmitter.broadcast({ type: 'bet' });
		} else if (!stopDisabled) {
			if (stateBetDerived.hasAutoBetCounter()) stateBet.autoSpinsCounter = 0;
			context.eventEmitter.broadcast({ type: 'stopButtonClick' });
		}
	};"""

old_markup = """	<!-- Spin / Stop : reutilise ButtonBetProvider pour la vraie logique,
	     sans le visuel par defaut (deja dans l'image de fond). -->
	<ButtonBetProvider>
		{#snippet children({ onpress, disabled })}
			<OnHotkey hotkey="Space" {disabled} {onpress} />
			<Container
				x={SPIN_X}
				y={ROW_Y}
				eventMode={disabled ? 'none' : 'static'}
				cursor={disabled ? 'not-allowed' : 'pointer'}
				onpointerup={onpress}
			>
				<Sprite width={180} height={180} alpha={0.001} />
			</Container>
		{/snippet}
	</ButtonBetProvider>"""
new_markup = """	<!-- Spin / Stop -->
	<OnHotkey hotkey="Space" disabled={spinDisabled} onpress={onSpinPress} />
	<Container
		x={SPIN_X}
		y={ROW_Y}
		eventMode={spinDisabled ? 'none' : 'static'}
		cursor={spinDisabled ? 'not-allowed' : 'pointer'}
		onpointerup={onSpinPress}
	>
		<Sprite width={180} height={180} alpha={0.001} />
	</Container>"""

missing = [n for n, o in [("import", old_import), ("logic", old_logic_anchor), ("markup", old_markup)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_logic_anchor, new_logic_anchor, 1)
    content = content.replace(old_markup, new_markup, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bouton spin reconstruit sans dependre de ButtonBetProvider.")
