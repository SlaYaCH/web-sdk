path = "apps/louvo/src/components/DevRevealPanel.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old_import = "import { getContext } from '../game/context';"
new_import = old_import + "\n\timport { stateBet } from 'state-shared';"
if old_import not in content:
    results.append("ERREUR (import) : ancre introuvable.")
else:
    content = content.replace(old_import, new_import, 1)
    results.append("OK (import) : stateBet importe.")

old_row = """<div class="dev-panel__row">
			<button onclick={() => setTier('basegame')}>Base</button>"""
new_row = """<div class="dev-panel__row">
			<button
				onclick={() => {
					stateBet.balanceAmount = 1000;
				}}
			>
				Crediter 1000
			</button>
		</div>
		<div class="dev-panel__row">
			<button onclick={() => setTier('basegame')}>Base</button>"""

count_row = content.count(old_row)
if count_row != 1:
    results.append(f"ERREUR (bouton) : trouve {count_row} fois (attendu 1).")
else:
    content = content.replace(old_row, new_row, 1)
    results.append("OK (bouton) : bouton 'Crediter 1000' ajoute au panneau dev.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
