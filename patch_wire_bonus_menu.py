path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import LouvoSettingsMenu from './LouvoSettingsMenu.svelte';"
new_import = old_import + "\n\timport LouvoBonusMenu from './LouvoBonusMenu.svelte';"

old_subscribe = """	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
	});"""
new_subscribe = """	let bonusMenuOpen = $state(false);

	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
		bonusMenuShow: () => (bonusMenuOpen = true),
	});"""

old_settings_block = """		{#if stateUi.menuOpen}
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
new_settings_block = old_settings_block + """

		{#if bonusMenuOpen}
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
				onpointerup={() => (bonusMenuOpen = false)}
			/>
			<Container
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
			>
				<LouvoBonusMenu />
			</Container>
		{/if}"""

missing = [n for n, o in [("import", old_import), ("subscribe", old_subscribe), ("settings_block", old_settings_block)] if o not in content]
if missing:
    print("ERREUR Game.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_subscribe, new_subscribe, 1)
    content = content.replace(old_settings_block, new_settings_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : ecran bonus branche, independant du menu reglages.")
