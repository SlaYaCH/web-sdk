path = "apps/louvo/src/components/LouvoBonusMenu.svelte"
with open(path, "r") as f:
    content = f.read()

old = """		<Sprite key={`louvoConfirm_${confirming.confirmKey}`} anchor={0.5} width={CONFIRM_WIDTH} height={CONFIRM_HEIGHT} />
		<Text
			anchor={0.5}
			y={CONFIRM_DESC_Y}"""
new = """		{@const isDateStack = confirming.confirmKey === 'speeddating' || confirming.confirmKey === 'afterdark'}
		<Sprite key={`louvoConfirm_${confirming.confirmKey}`} anchor={0.5} width={CONFIRM_WIDTH} height={CONFIRM_HEIGHT} />
		<Text
			anchor={0.5}
			y={isDateStack ? 0.8 * CONFIRM_HEIGHT - CONFIRM_HEIGHT / 2 : CONFIRM_DESC_Y}"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : texte descendu pour les confirmations 3-DATE et 4-DATE uniquement.")
