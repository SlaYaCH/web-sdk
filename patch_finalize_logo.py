results = []

# --- 1) +layout.svelte : retirer LoaderExample, ajouter LouvoLoaderLogo ---
path = "apps/louvo/src/routes/+layout.svelte"
with open(path, "r") as f:
    c = f.read()

old_a = "import { Authenticate, LoaderStakeEngine, LoaderExample, LoadI18n } from 'components-shared';\n\timport Game from '../components/Game.svelte';"
new_a = "import { Authenticate, LoaderStakeEngine, LoadI18n } from 'components-shared';\n\timport Game from '../components/Game.svelte';\n\timport LouvoLoaderLogo from '../components/LouvoLoaderLogo.svelte';"
n = c.count(old_a)
if n != 1:
    results.append(f"ERREUR (import) : trouve {n} fois.")
else:
    c = c.replace(old_a, new_a, 1)
    results.append("OK (import)")

old_b = "const loaderUrl = new URL('../../loader.gif', import.meta.url).href;"
new_b = "const loaderUrl = new URL('../../louvo_logo.png', import.meta.url).href;"
n = c.count(old_b)
if n != 1:
    results.append(f"ERREUR (loaderUrl) : trouve {n} fois.")
else:
    c = c.replace(old_b, new_b, 1)
    results.append("OK (loaderUrl)")

old_c = """	<LoaderExample src={loaderUrl} />
	<!-- '/loader.gif' is served from static folder of sveltekit -->
	<!-- File location: apps/scatter/static/loader.gif -->"""
new_c = "\t<LouvoLoaderLogo src={loaderUrl} />"
n = c.count(old_c)
if n != 1:
    results.append(f"ERREUR (usage) : trouve {n} fois - tentative avec espaces...")
    old_c2 = old_c.replace("\t", "        ")
    n2 = c.count(old_c2)
    if n2 == 1:
        c = c.replace(old_c2, new_c, 1)
        results.append("OK (usage, variante espaces)")
    else:
        results.append(f"ERREUR (usage, variante espaces aussi) : {n2} fois.")
else:
    c = c.replace(old_c, new_c, 1)
    results.append("OK (usage)")

with open(path, "w") as f:
    f.write(c)

# --- 2) Game.svelte : remplacer le texte par le vrai logo ---
path2 = "apps/louvo/src/components/Game.svelte"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """			<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
				<Text
					anchor={{ x: 1, y: 0 }}
					text="ADD YOUR LOGO"
					style={{
						fontFamily: 'proxima-nova',
						fontSize: REM * 1.5,
						fontWeight: '600',
						lineHeight: REM * 2,
						fill: 0xffffff,
					}}
				/>
			</Container>"""
new2 = """			<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
				<Sprite key="louvoLogo" anchor={{ x: 1, y: 0 }} width={100} height={72.8} />
			</Container>"""

n2 = c2.count(old2)
if n2 != 1:
    results.append(f"ERREUR (Game.svelte) : trouve {n2} fois (attendu 1) - verification manuelle necessaire.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK (Game.svelte) : texte remplace par le vrai logo (badge ~100x73px, coin haut droit).")

for r in results:
    print(r)
