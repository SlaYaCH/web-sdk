path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { UI, UiGameName } from 'components-ui-pixi';"
new_import = "import { UiGameName } from 'components-ui-pixi';\nimport LouvoBottomBar from './LouvoBottomBar.svelte';"

old_ui_block = """		<UI>
			{#snippet gameName()}
				<UiGameName name="LINES GAME" />
			{/snippet}
			{#snippet logo()}
				<Text
					anchor={{ x: 1, y: 0 }}
					text="ADD YOUR LOGO"
					style={{
						fontFamily: 'proxima-nova',
						fontSize: REM * 1.5,
						fontWeight: '600',
						lineHeight: REM * 2,
						fill: 0xffffff,
					}}
				/>
			{/snippet}
		</UI>"""
new_ui_block = """		<Container x={20}>
			<UiGameName name="LINES GAME" />
		</Container>
		<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
			<Text
				anchor={{ x: 1, y: 0 }}
				text="ADD YOUR LOGO"
				style={{
					fontFamily: 'proxima-nova',
					fontSize: REM * 1.5,
					fontWeight: '600',
					lineHeight: REM * 2,
					fill: 0xffffff,
				}}
			/>
		</Container>
		<MainContainer standard alignVertical="bottom">
			<Container
				x={context.stateLayoutDerived.mainLayoutStandard().width * 0.5}
				y={context.stateLayoutDerived.mainLayoutStandard().height - 10}
			>
				<LouvoBottomBar />
			</Container>
		</MainContainer>"""

missing = [n for n, o in [("import", old_import), ("ui_block", old_ui_block)] if o not in content]
if missing:
    print("ERREUR Game.svelte : ancre(s) introuvable(s) (peut-etre deja fait) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_ui_block, new_ui_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Game.svelte utilise LouvoBottomBar a la place de la barre generique.")
