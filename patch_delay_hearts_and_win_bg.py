results = []

# --- 1) Retarder le lancer des coeurs (laisser les rouleaux se poser d'abord) ---
path1 = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1 = "const BASE_DELAY = 300;"
new1 = "const BASE_DELAY = 900; // laisse le temps aux rouleaux de finir de se poser"
n = c1.count(old1)
if n != 1:
    results.append(f"ERREUR (BASE_DELAY) : {n} fois.")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK (BASE_DELAY) : 300ms -> 900ms avant le premier coeur.")

# --- 2) Fond noir transparent derriere le gain, pour TOUS les gains (pas juste big win) ---
path2 = "apps/louvo/src/components/Win.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """				{#if isBigWin}
					<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />
				{/if}"""
new2 = """				<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />"""
n = c2.count(old2)
if n != 1:
    results.append(f"ERREUR (fond gain) : {n} fois - verification manuelle necessaire.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK (fond gain) : fond noir transparent maintenant sur TOUS les gains, pas que big win.")

for r in results:
    print(r)
