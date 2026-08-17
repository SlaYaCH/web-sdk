path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

# --- 1) Corriger le texte MATCH : duel entre deux MULTIPLICATEURS, pas deux symboles ---
old_match = "<p>When two MATCH symbols land, they face off in a duel. Each side is dealt a multiplier, and only one wins the exchange, either could take it. The surviving multiplier is applied to the win.</p>"
new_match = "<p>When MATCH symbols land in a winning combination, two multiplier values face off in a duel. Either one can win, it's a coin flip, and only the surviving multiplier is applied to the win.</p>"

if old_match not in content:
    print("ERREUR : texte MATCH introuvable.")
else:
    content = content.replace(old_match, new_match, 1)
    print("OK : texte MATCH corrige (duel de multiplicateurs, pas de symboles).")

old_special_match = "<p><strong>MATCH</strong> triggers a duel between two symbols, deciding a multiplier for the win.</p>"
new_special_match = "<p><strong>MATCH</strong> triggers a duel between two multiplier values, deciding the multiplier applied to the win.</p>"

if old_special_match not in content:
    print("ERREUR : texte MATCH (symboles speciaux) introuvable.")
else:
    content = content.replace(old_special_match, new_special_match, 1)
    print("OK : texte MATCH corrige dans SPECIAL SYMBOLS aussi.")

# --- 2) Generer les 19 diagrammes de lignes a partir des vraies donnees config.ts ---
paylines = {
    1: [0,0,0,0,0], 2: [1,1,1,1,1], 3: [2,2,2,2,2], 4: [3,3,3,3,3], 5: [4,4,4,4,4],
    6: [0,1,1,1,0], 7: [4,3,3,3,4], 8: [1,2,2,2,1], 9: [3,2,2,2,3], 10: [2,1,1,1,2],
    11: [2,3,3,3,2], 12: [0,0,1,0,0], 13: [4,4,3,4,4], 14: [1,1,0,1,1], 15: [3,3,4,3,3],
    16: [1,1,2,1,1], 17: [3,3,2,3,3], 18: [0,1,2,1,0], 19: [4,3,2,3,4],
}

def grid_html(line_num, rows):
    cells = []
    for row in range(5):
        for col in range(5):
            active = rows[col] == row
            cls = "ln-cell active" if active else "ln-cell"
            cells.append(f'<div class="{cls}"></div>')
    grid = "".join(cells)
    return f'<div class="ln-item"><div class="ln-label">{line_num}</div><div class="ln-grid">{grid}</div></div>'

items = "".join(grid_html(n, r) for n, r in paylines.items())
paylines_html = f'<div class="ln-wrap">{items}</div>'

old_ways = '<p>You win when matching symbols land on adjacent reels, starting from the leftmost reel, along one of 19 fixed paylines. Only the highest win per line is paid.</p>'
new_ways = old_ways + "\n\t" + paylines_html

if old_ways not in content:
    print("ERREUR : section WAYS TO WIN introuvable.")
else:
    content = content.replace(old_ways, new_ways, 1)
    print("OK : 19 diagrammes de lignes inseres.")

# --- 3) CSS pour les diagrammes ---
old_css_marker = "\t.louvo-paytable-item span {\n\t\tdisplay: block;\n\t}\n</style>"
new_css = """	.louvo-paytable-item span {
		display: block;
	}
	.ln-wrap {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
		gap: 10px;
		margin: 12px 0;
	}
	.ln-item {
		text-align: center;
	}
	.ln-label {
		font-size: 11px;
		color: #ff8fb3;
		margin-bottom: 2px;
	}
	.ln-grid {
		display: grid;
		grid-template-columns: repeat(5, 8px);
		grid-template-rows: repeat(5, 8px);
		gap: 1px;
		background: #000000;
		padding: 2px;
		margin: 0 auto;
		width: fit-content;
	}
	.ln-cell {
		width: 8px;
		height: 8px;
		background: #2a1018;
	}
	.ln-cell.active {
		background: #ff2d6a;
	}
</style>"""

if old_css_marker not in content:
    print("ERREUR : marqueur CSS introuvable.")
else:
    content = content.replace(old_css_marker, new_css, 1)
    print("OK : CSS des diagrammes ajoute.")

with open(path, "w") as f:
    f.write(content)
