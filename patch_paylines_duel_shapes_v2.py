path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

def grid_html(line_num, rows):
    cells = []
    for row in range(5):
        for col in range(5):
            active = rows[col] == row
            cls = "ln-cell active" if active else "ln-cell"
            cells.append(f'<div class="{cls}"></div>')
    grid = "".join(cells)
    return f'<div class="ln-item"><div class="ln-label">{line_num}</div><div class="ln-grid">{grid}</div></div>'

def build_html(paylines):
    items = "".join(grid_html(n, r) for n, r in paylines.items())
    return f'<div class="ln-wrap">{items}</div>'

old_paylines = {
    1: [0,0,0,0,0], 2: [1,1,1,1,1], 3: [2,2,2,2,2], 4: [3,3,3,3,3], 5: [4,4,4,4,4],
    6: [0,1,1,1,0], 7: [4,3,3,3,4], 8: [1,2,2,2,1], 9: [3,2,2,2,3], 10: [2,1,1,1,2],
    11: [2,3,3,3,2], 12: [0,0,1,0,0], 13: [4,4,3,4,4], 14: [1,1,0,1,1], 15: [3,3,4,3,3],
    16: [1,1,2,1,1], 17: [3,3,2,3,3], 18: [0,1,2,1,0], 19: [4,3,2,3,4],
}
new_paylines = {
    1: [0,0,0,0,0], 2: [1,1,1,1,1], 3: [2,2,2,2,2], 4: [3,3,3,3,3], 5: [4,4,4,4,4],
    6: [0,1,0,1,0], 7: [1,2,1,2,1], 8: [2,3,2,3,2], 9: [3,4,3,4,3], 10: [1,0,1,0,1],
    11: [2,1,2,1,2], 12: [3,2,3,2,3], 13: [4,3,4,3,4], 14: [0,1,2,3,4], 15: [1,2,3,2,1],
    16: [2,3,4,3,2], 17: [4,3,2,1,0], 18: [3,2,1,2,3], 19: [2,1,0,1,2],
}

old_html = build_html(old_paylines)
new_html = build_html(new_paylines)

count = content.count(old_html)
if count != 1:
    print(f"ERREUR : ancien bloc HTML trouve {count} fois (attendu 1).")
else:
    content = content.replace(old_html, new_html, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les 19 diagrammes remplaces par les vraies formes de Duel at Dawn.")
