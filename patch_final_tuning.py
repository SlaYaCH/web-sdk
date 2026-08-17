# --- SuperlikeBarilletDisplay.svelte : taille + position + resynchro sur le lancer sequentiel ---
path = "apps/louvo/src/components/SuperlikeBarilletDisplay.svelte"
with open(path, "r") as f:
    content = f.read()

old_hub = "const HUB_Y = 154;"
new_hub = "const HUB_Y = 152.5;"

old_size = "const HEART_SIZE = 58;"
new_size = "const HEART_SIZE = 50;"

old_stagger = "const THROW_STAGGER = 80;"
new_stagger = "const THROW_STAGGER = 550; // doit correspondre a la duree d'un vol dans SuperlikeHeartThrow (lancer sequentiel)"

missing = [n for n, o in [("hub", old_hub), ("size", old_size), ("stagger", old_stagger)] if o not in content]
if missing:
    print("ERREUR SuperlikeBarilletDisplay.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_hub, new_hub, 1)
    content = content.replace(old_size, new_size, 1)
    content = content.replace(old_stagger, new_stagger, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : HUB_Y=152.5, coeurs a 50px, synchro mise a jour pour le lancer sequentiel.")

# --- SuperlikeHeartThrow.svelte : lancer sequentiel (un coeur a la fois) ---
path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old_throw = """	const throwHeart = (index: number, delay: number) =>
		new Promise<void>((resolve) => {
			const target = targets[index];
			const duration = 550;
			const arcHeight = 60 + Math.random() * 30;
			const start = performance.now() + delay;

			const step = (now: number) => {
				const elapsed = now - start;
				if (elapsed < 0) {
					requestAnimationFrame(step);
					return;
				}
				const t = Math.min(elapsed / duration, 1);
				const eased = easeOutQuad(t);

				hearts[index].x = originX + (target.x - originX) * eased;
				hearts[index].y =
					originY + (target.y - originY) * eased - Math.sin(t * Math.PI) * arcHeight;
				hearts[index].alpha = t < 0.15 ? t / 0.15 : 1;
				hearts[index].scale = 0.5 + Math.min(t / 0.2, 1) * 0.5;

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					fadeOut(index).then(resolve);
				}
			};

			requestAnimationFrame(step);
		});

	onMount(() => {
		hearts.forEach((_, index) => {
			throwHeart(index, BASE_DELAY + index * 80);
		});
	});"""

new_throw = """	// Vole vers la cible et resout des que le coeur touche sa case - le
	// fondu de disparition part APRES en arriere-plan (fire-and-forget),
	// sans retarder le lancer du coeur suivant.
	const flyTo = (index: number) =>
		new Promise<void>((resolve) => {
			const target = targets[index];
			const duration = 550;
			const arcHeight = 60 + Math.random() * 30;
			const start = performance.now();

			const step = (now: number) => {
				const elapsed = now - start;
				const t = Math.min(elapsed / duration, 1);
				const eased = easeOutQuad(t);

				hearts[index].x = originX + (target.x - originX) * eased;
				hearts[index].y =
					originY + (target.y - originY) * eased - Math.sin(t * Math.PI) * arcHeight;
				hearts[index].alpha = t < 0.15 ? t / 0.15 : 1;
				hearts[index].scale = 0.5 + Math.min(t / 0.2, 1) * 0.5;

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					resolve();
					fadeOut(index);
				}
			};

			requestAnimationFrame(step);
		});

	onMount(() => {
		(async () => {
			await new Promise((r) => setTimeout(r, BASE_DELAY));
			for (let i = 0; i < hearts.length; i++) {
				await flyTo(i);
			}
		})();
	});"""

if old_throw not in content:
    print("ERREUR SuperlikeHeartThrow.svelte : ancre introuvable.")
else:
    content = content.replace(old_throw, new_throw, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : lancer des coeurs rendu sequentiel (un a la fois, attend l'arrivee avant le suivant).")

# --- SpecialRevealOverlay.svelte : banniere affichee plus longtemps ---
path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_holdms = "holdMs={2500}"
new_holdms = "holdMs={6000}"

if old_holdms not in content:
    print("ERREUR SpecialRevealOverlay.svelte : ancre introuvable.")
else:
    content = content.replace(old_holdms, new_holdms, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : banniere affichee 6s au lieu de 2.5s (laisse le temps au lancer sequentiel de 6 coeurs max de se terminer).")
