path = "apps/louvo/src/components/Win.svelte"
with open(path, "r") as f:
    content = f.read()

old = """				<OnMount
					onmount={async () => {
						await startCountUp();
						await waitForTimeout(300);
						oncomplete();
					}}
				/>"""

new = """				<OnMount
					onmount={async () => {
						await startCountUp();
						await waitForTimeout(300);
						// Reste affiche jusqu'au prochain spin (ou un clic manuel via
						// PressToContinue) - plus de fermeture automatique ici.
					}}
				/>"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : fermeture automatique retiree, le gain reste affiche jusqu'au prochain spin.")
