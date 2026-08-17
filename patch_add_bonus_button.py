path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old_const = "const AUTOSPIN_X = BAR_WIDTH * 0.970 - BAR_WIDTH / 2;"
new_const = old_const + "\n\tconst BONUS_X = -BAR_WIDTH / 2 - 90;"

old_menu_logic = """	// --- Menu (identique a ButtonMenu.svelte) ---
	const onMenu = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateUi.menuOpen = true;
	};"""
new_menu_logic = old_menu_logic + """

	// --- Bonus (ouvre l'ecran d'achat de bonus, evenement dedie) ---
	const onBonus = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		context.eventEmitter.broadcast({ type: 'bonusMenuShow' });
	};"""

old_markup = """	<!-- Menu -->
	<Container
		x={MENU_X}
		y={ROW_Y}
		eventMode="static"
		cursor="pointer"
		onpointerup={onMenu}
	>
		<Sprite width={100} height={100} alpha={0.001} />
	</Container>"""
new_markup = """	<!-- Bonus -->
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
	</Container>

	<!-- Menu -->
	<Container
		x={MENU_X}
		y={ROW_Y}
		eventMode="static"
		cursor="pointer"
		onpointerup={onMenu}
	>
		<Sprite width={100} height={100} alpha={0.001} />
	</Container>"""

old_import = "import { Container, Sprite, Text } from 'pixi-svelte';"
new_import = "import { Container, Sprite, Text, Rectangle } from 'pixi-svelte';"

missing = [n for n, o in [("const", old_const), ("menu_logic", old_menu_logic), ("markup", old_markup), ("import", old_import)] if o not in content]
if missing:
    print("ERREUR LouvoBottomBar.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_const, new_const, 1)
    content = content.replace(old_menu_logic, new_menu_logic, 1)
    content = content.replace(old_markup, new_markup, 1)
    content = content.replace(old_import, new_import, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : bouton BONUS ajoute a gauche du menu.")
