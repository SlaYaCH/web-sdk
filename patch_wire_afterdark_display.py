path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old_import = "import LouvoBottomBar from './LouvoBottomBar.svelte';"
count_i = content.count(old_import)
if count_i != 1:
    results.append(f"ERREUR import : trouve {count_i} fois (attendu 1).")
else:
    new_import = old_import + "\n\timport AfterDarkStreakDisplay from './AfterDarkStreakDisplay.svelte';"
    content = content.replace(old_import, new_import, 1)
    results.append("OK : import ajoute.")

old_usage = "<BoardFrame />"
count_u = content.count(old_usage)
if count_u != 1:
    results.append(f"ERREUR usage : trouve {count_u} fois (attendu 1).")
else:
    new_usage = (
        old_usage
        + "\n\t\t\t\t<AfterDarkStreakDisplay\n"
        + "\t\t\t\t\ttier2={{ filled: 6, achieved: true }}\n"
        + "\t\t\t\t\ttier3={{ filled: 3, achieved: false }}\n"
        + "\t\t\t\t\ttier4={{ filled: 0, achieved: false }}\n"
        + "\t\t\t\t\ttier5x={{ filled: 2, achieved: false }}\n"
        + "\t\t\t\t/>"
    )
    content = content.replace(old_usage, new_usage, 1)
    results.append("OK : composant insere avec des valeurs de test.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
