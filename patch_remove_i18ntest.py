path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "\timport I18nTest from './I18nTest.svelte';\n"
count1 = content.count(old1)
if count1 != 1:
    results.append(f"ERREUR (import) : trouve {count1} fois (attendu 1).")
else:
    content = content.replace(old1, "", 1)
    results.append("OK (import) : retire.")

old2 = "\t\t<I18nTest />\n"
count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (usage) : trouve {count2} fois (attendu 1).")
else:
    content = content.replace(old2, "", 1)
    results.append("OK (usage) : retire, le bandeau de debug ne s'affichera plus.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
