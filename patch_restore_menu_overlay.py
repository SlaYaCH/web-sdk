path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_import1 = "import { App, Text, REM, Container } from 'pixi-svelte';"
new_import1 = "import { App, Text, REM, Container, Rectangle } from 'pixi-svelte';"

old_import2 = "import { UiGameName } from 'components-ui-pixi';\nimport LouvoBottomBar from './LouvoBottomBar.svelte';"
new_import2 = """import { UiGameName, ButtonPayTable, ButtonGameRules, ButtonSettings, ButtonSoundSwitch, ButtonMenuClose } from 'components-ui-pixi';
	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import LouvoBottomBar from './LouvoBottomBar.svelte';"""

old_bar_block = """		<MainContainer standard alignVertical="bottom">
			<Container
				x={context.stateLayoutDerived.mainLayoutStandard().width * 0.5}
				y={context.stateLayoutDerived.mainLayoutStandard().height - 10}
			>
				<LouvoBottomBar />
			</Container>
		</MainContainer>"""
new_bar_block = old_bar_block + """

		{#if stateUi.menuOpen}
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

missing = [n for n, o in [("import1", old_import1), ("import2", old_import2), ("bar_block", old_bar_block)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import1, new_import1, 1)
    content = content.replace(old_import2, new_import2, 1)
    content = content.replace(old_bar_block, new_bar_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : panneau menu restaure (version provisoire, boutons generiques).")
