path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	.dev-panel {
		position: fixed;
		bottom: 8px;
		left: 8px;
		z-index: 9999;
		background: rgba(0, 0, 0, 0.75);
		border: 1px solid #ff4d8d;
		border-radius: 8px;
		padding: 8px;
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-family: sans-serif;
		font-size: 12px;
	}
	.dev-panel__row {
		display: flex;
		gap: 4px;
		align-items: center;
	}"""

new = """	.dev-panel {
		position: fixed;
		top: 8px;
		bottom: 8px;
		left: 8px;
		width: 140px;
		z-index: 9999;
		background: rgba(0, 0, 0, 0.75);
		border: 1px solid #ff4d8d;
		border-radius: 8px;
		padding: 8px;
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-family: sans-serif;
		font-size: 12px;
		overflow-y: auto;
	}
	.dev-panel__row {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		align-items: center;
	}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : panneau dev deplace en bande verticale dans la marge gauche (140px, pleine hauteur, renvoi a la ligne).")
