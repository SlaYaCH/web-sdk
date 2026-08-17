path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = """						if (reelSymbol) {
							reelSymbol.rawSymbol = { name: 'W', wild: true };
						}
					}
					// Le coeur disparait immediatement"""

new = """						if (reelSymbol) {
							reelSymbol.rawSymbol = { name: 'W', wild: true };
						}
					}
					context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
					// Le coeur disparait immediatement"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : sfx_wild_explode joue exactement quand le wild apparait.")
