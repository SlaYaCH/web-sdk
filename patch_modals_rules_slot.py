path = "packages/components-ui-html/src/components/Modals.svelte"
with open(path, "r") as f:
    content = f.read()

old_props = """	type Props = {
		version: Snippet;
	};
	const props: Props = $props();"""
new_props = """	type Props = {
		version: Snippet;
		gameRules?: Snippet;
		payTable?: Snippet;
	};
	const props: Props = $props();"""

old_modals = """<ModalPayTable>
	{@render props.version()}
</ModalPayTable>
<ModalGameRules>
	{@render props.version()}
</ModalGameRules>"""
new_modals = """<ModalPayTable>
	{#if props.payTable}
		{@render props.payTable()}
	{:else}
		{@render props.version()}
	{/if}
</ModalPayTable>
<ModalGameRules>
	{#if props.gameRules}
		{@render props.gameRules()}
	{:else}
		{@render props.version()}
	{/if}
</ModalGameRules>"""

missing = [n for n, o in [("props", old_props), ("modals", old_modals)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_props, new_props, 1)
    content = content.replace(old_modals, new_modals, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : gameRules et payTable ont maintenant leur propre emplacement (optionnel, ne casse rien pour les autres jeux du monorepo).")
