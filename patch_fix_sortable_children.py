path = "apps/louvo/src/components/BoardContainer.svelte"
with open(path, "r") as f:
    content = f.read()

old = """<Container
	x={context.stateGameDerived.boardLayout().x}
	y={context.stateGameDerived.boardLayout().y}
	pivot={context.stateGameDerived.boardLayout().pivot}
>"""
new = """<Container
	x={context.stateGameDerived.boardLayout().x}
	y={context.stateGameDerived.boardLayout().y}
	pivot={context.stateGameDerived.boardLayout().pivot}
	sortableChildren={true}
>"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : sortableChildren active - TOUS les zIndex (lignes gagnantes, coeurs, bannieres) vont enfin vraiment fonctionner.")
