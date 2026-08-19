results = []

# --- 1) SpecialRevealOverlay.svelte : forceClose booleen -> closeToken numerique ---
path1 = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1a = "let forceClose = $state(false);"
new1a = "let closeToken = $state(0);"
n = c1.count(old1a)
if n != 1:
    results.append(f"ERREUR (declaration) : {n} fois.")
else:
    c1 = c1.replace(old1a, new1a, 1)
    results.append("OK (declaration closeToken)")

old1b = "if (show) forceClose = true;"
new1b = "if (show) closeToken += 1;"
n = c1.count(old1b)
if n != 1:
    results.append(f"ERREUR (increment) : {n} fois.")
else:
    c1 = c1.replace(old1b, new1b, 1)
    results.append("OK (increment sur spinStart)")

old1c = "\t\t\tforceClose = false;\n"
new1c = ""
n = c1.count(old1c)
if n != 1:
    results.append(f"ERREUR (retrait reset) : {n} fois.")
else:
    c1 = c1.replace(old1c, new1c, 1)
    results.append("OK (retrait de l'ancien reset, plus necessaire)")

old1d = "forceClose={forceClose}"
new1d = "closeToken={closeToken}"
n = c1.count(old1d)
if n != 1:
    results.append(f"ERREUR (passage prop) : {n} fois.")
else:
    c1 = c1.replace(old1d, new1d, 1)
    results.append("OK (passage closeToken au lieu de forceClose)")

with open(path1, "w") as f:
    f.write(c1)

# --- 2) BannerReveal.svelte : accepter closeToken, comparer a une valeur de reference ---
path2 = "apps/louvo/src/components/BannerReveal.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2a = "forceClose?: boolean;"
new2a = "closeToken?: number;"
n = c2.count(old2a)
if n != 1:
    results.append(f"ERREUR (type prop) : {n} fois.")
else:
    c2 = c2.replace(old2a, new2a, 1)
    results.append("OK (type prop closeToken)")

old2b = """	$effect(() => {
		if (props.forceClose) resolveHold();
	});"""
new2b = """	// Valeur de reference capturee au montage : tout changement ulterieur
	// de closeToken (peu importe l'ancienne valeur booleenne ratee en
	// turbo/super turbo) declenche la fermeture, sans jamais pouvoir etre
	// rate meme si plusieurs spins s'enchainent tres vite.
	const initialCloseToken = props.closeToken;
	$effect(() => {
		if (props.closeToken !== undefined && props.closeToken !== initialCloseToken) resolveHold();
	});"""
n = c2.count(old2b)
if n != 1:
    results.append(f"ERREUR (effect) : {n} fois.")
else:
    c2 = c2.replace(old2b, new2b, 1)
    results.append("OK (effect base sur closeToken)")

with open(path2, "w") as f:
    f.write(c2)

for r in results:
    print(r)
