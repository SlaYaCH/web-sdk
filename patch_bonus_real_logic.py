path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old_import_state = "import { stateBet, stateBetDerived, stateConfig, stateUi, stateModal } from 'state-shared';"
if old_import_state not in content:
    print("ERREUR : import state-shared introuvable (deja modifie ?).")
else:
    pass

old_bonus_logic = """	// --- Bonus (ouvre l'ecran d'achat de bonus, evenement dedie) ---
	const onBonus = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		context.eventEmitter.broadcast({ type: 'bonusMenuShow' });
	};"""
new_bonus_logic = """	// --- Bonus (logique identique a ButtonBuyBonus.svelte reel) ---
	const bonusActive = $derived(stateBetDerived.activeBetMode()?.type === 'activate');
	const bonusDisabled = $derived(!context.stateXstateDerived.isIdle());
	const onBonus = () => {
		if (bonusDisabled) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (bonusActive) {
			stateBet.activeBetModeKey = 'BASE';
		} else {
			stateModal.modal = { name: 'buyBonus' };
		}
	};"""

old_markup = """	<!-- Bonus -->
	<Container
		x={BONUS_X}
		y={ROW_Y}
		eventMode="static"
		cursor="pointer"
		onpointerup={onBonus}
	>
		<Rectangle anchor={0.5} width={120} height={60} backgroundColor={0xff2d6a} borderColor={0xffffff} borderWidth={2} />
		<Text
			anchor={0.5}
			text="BONUS"
			style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 20, fill: 0xffffff }}
		/>
	</Container>"""
new_markup = """	<!-- Bonus -->
	<Container
		x={BONUS_X}
		y={ROW_Y}
		eventMode={bonusDisabled ? 'none' : 'static'}
		cursor={bonusDisabled ? 'not-allowed' : 'pointer'}
		alpha={bonusDisabled ? 0.5 : 1}
		onpointerup={onBonus}
	>
		<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
		{#if bonusActive}
			<Rectangle anchor={0.5} width={90} height={90} backgroundColor={0x000000} alpha={0} borderColor={0xffffff} borderWidth={4} />
		{/if}
	</Container>"""

missing = [n for n, o in [("bonus_logic", old_bonus_logic), ("markup", old_markup)] if o not in content]
if missing:
    print("ERREUR LouvoBottomBar.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_bonus_logic, new_bonus_logic, 1)
    content = content.replace(old_markup, new_markup, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bouton bonus branche sur le vrai mecanisme + vraie icone.")
