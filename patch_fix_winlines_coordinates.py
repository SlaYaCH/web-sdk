path = "apps/louvo/src/components/WinLinesDisplay.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old_import = "import WinLineReveal from './WinLineReveal.svelte';"
new_import = old_import + "\n\timport BoardContainer from './BoardContainer.svelte';"
if old_import not in content:
    results.append("ERREUR (import) : ancre introuvable.")
else:
    content = content.replace(old_import, new_import, 1)
    results.append("OK (import) : BoardContainer importe.")

old_template = """<Container>
	{#each activeWins as win (win.id)}
		<WinLineReveal positions={win.positions} amount={win.amount} oncomplete={() => remove(win.id)} />
	{/each}
</Container>"""
new_template = """<BoardContainer>
	{#snippet children()}
		{#each activeWins as win (win.id)}
			<WinLineReveal positions={win.positions} amount={win.amount} oncomplete={() => remove(win.id)} />
		{/each}
	{/snippet}
</BoardContainer>"""

count = content.count(old_template)
if count != 1:
    results.append(f"ERREUR (template) : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old_template, new_template, 1)
    results.append("OK (template) : les lignes de gain utilisent maintenant le meme repere que le vrai plateau (BoardContainer).")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
