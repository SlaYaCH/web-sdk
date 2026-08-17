path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old = """			if (holdMs > 0) {
				await Promise.race([
					new Promise<void>((r) => setTimeout(r, holdMs)),
					new Promise<void>((r) => (resolveHold = r)),
				]);
				await animateTo(1, 0, Math.min(durationInMs, 250));
			}"""

new = """			if (holdMs > 0) {
				if (holdMs === Infinity) {
					// Pas de minuteur du tout : attend uniquement forceClose
					// (prochain spin), jamais de fermeture automatique.
					await new Promise<void>((r) => (resolveHold = r));
				} else {
					await Promise.race([
						new Promise<void>((r) => setTimeout(r, holdMs)),
						new Promise<void>((r) => (resolveHold = r)),
					]);
				}
				await animateTo(1, 0, Math.min(durationInMs, 250));
			}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : ancre introuvable (trouve {count} fois).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : holdMs=Infinity attend maintenant vraiment forceClose, sans minuteur du tout.")
