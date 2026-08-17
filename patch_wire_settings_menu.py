path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import LouvoBottomBar from './LouvoBottomBar.svelte';"
new_import = "import LouvoBottomBar from './LouvoBottomBar.svelte';\n\timport LouvoSettingsMenu from './LouvoSettingsMenu.svelte';"

old_block = """		{#if stateUi.menuOpen}
			<Rectangle
				eventMode="static"
				cursor="pointer"
				alpha={0.5}
				anchor={0.5}
				backgroundColor={BLACK}
				width={context.stateLayoutDerived.canvasSizes().width}
				height={context.stateLayoutDerived.canvasSizes().height}
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
				onpointerup={() => (stateUi.menuOpen = false)}
			/>
			<MainContainer standard alignVertical="bottom">
				<Container
					x={298}
					y={context.stateLayoutDerived.mainLayoutStandard().height - 145 - 10}
				>
					<Container scale={0.8} y={-170 * 3}>
						<ButtonPayTable anchor={0.5} />
					</Container>
					<Container scale={0.8} y={-170 * 2}>
						<ButtonGameRules anchor={0.5} />
					</Container>
					<Container scale={0.8} y={-170 * 1}>
						<ButtonSettings anchor={0.5} />
					</Container>
					<Container scale={0.8} y={0}>
						<ButtonSoundSwitch anchor={0.5} />
					</Container>
					<Container scale={0.8} y={170}>
						<ButtonMenuClose anchor={0.5} />
					</Container>
				</Container>
			</MainContainer>
		{/if}"""
new_block = """		{#if stateUi.menuOpen}
			<Rectangle
				eventMode="static"
				cursor="pointer"
				alpha={0.5}
				anchor={0.5}
				backgroundColor={BLACK}
				width={context.stateLayoutDerived.canvasSizes().width}
				height={context.stateLayoutDerived.canvasSizes().height}
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
				onpointerup={() => (stateUi.menuOpen = false)}
			/>
			<Container
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
			>
				<LouvoSettingsMenu />
			</Container>
		{/if}"""

missing = [n for n, o in [("import", old_import), ("block", old_block)] if o not in content]
if missing:
    print("ERREUR Game.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Game.svelte utilise le vrai menu Louvo a la place des boutons generiques.")
