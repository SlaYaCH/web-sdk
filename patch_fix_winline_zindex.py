path = "apps/louvo/src/components/WinLineReveal.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "<Container alpha={lineAlpha}>"
new1 = "<Container alpha={lineAlpha} zIndex={40}>"
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (ligne) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (ligne)")

old2 = "<Container x={midX} y={midY - AMOUNT_Y_OFFSET} alpha={amountAlpha}>"
new2 = "<Container x={midX} y={midY - AMOUNT_Y_OFFSET} alpha={amountAlpha} zIndex={40}>"
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (montant) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (montant)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
