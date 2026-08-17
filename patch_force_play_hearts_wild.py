path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up' });"
count1 = content.count(old1)
if count1 != 1:
    results.append(f"ERREUR (son vol) : trouve {count1} fois (attendu 1).")
else:
    content = content.replace(
        old1,
        "context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up', forcePlay: true });",
        1,
    )
    results.append("OK (son vol) : forcePlay ajoute.")

old2 = "context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });"
count2 = content.count(old2)
if count2 != 1:
    results.append(f"ERREUR (son wild) : trouve {count2} fois (attendu 1).")
else:
    content = content.replace(
        old2,
        "context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode', forcePlay: true });",
        1,
    )
    results.append("OK (son wild) : forcePlay ajoute.")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
