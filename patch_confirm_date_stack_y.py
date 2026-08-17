path = "apps/louvo/src/components/LouvoBonusMenu.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	{:else if option.confirmKey}
		<Sprite key={`louvoConfirm_${option.confirmKey}`} anchor={0.5} width={CONFIRM_WIDTH} height={CONFIRM_HEIGHT} />
		<Text
			anchor={0.5}
			y={CONFIRM_DESC_Y}"""
new = """	{:else if option.confirmKey}
		{@const isDateStack = option.confirmKey === 'speeddating' || option.confirmKey === 'afterdark'}
		<Sprite key={`louvoConfirm_${option.confirmKey}`} anchor={0.5} width={CONFIRM_WIDTH} height={CONFIRM_HEIGHT} />
		<Text
			anchor={0.5}
			y={isDateStack ? 0.8 * CONFIRM_HEIGHT - CONFIRM_HEIGHT / 2 : CONFIRM_DESC_Y}"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : texte descendu specifiquement pour les confirmations 3-DATE et 4-DATE (pile plus haute que les autres cartes).")
