path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "\timport { Container, Sprite } from 'pixi-svelte';"
new1 = "\timport { Container, Sprite, Rectangle } from 'pixi-svelte';"
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (import Rectangle) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (import Rectangle)")

old2 = "\tconst { BOARD_SIZES, SYMBOL_HEIGHT, REEL_PADDING } = "
# On importe aussi SYMBOL_SIZE pour dimensionner le cache
old2b = "import { BOARD_SIZES, SYMBOL_HEIGHT, REEL_PADDING } from '../game/constants';"
new2b = "import { BOARD_SIZES, SYMBOL_HEIGHT, SYMBOL_SIZE, REEL_PADDING } from '../game/constants';"
n = content.count(old2b)
if n != 1:
    results.append(f"ERREUR (import SYMBOL_SIZE) : {n} fois.")
else:
    content = content.replace(old2b, new2b, 1)
    results.append("OK (import SYMBOL_SIZE)")

old3 = """	type Heart = { id: number; x: number; y: number; alpha: number; scale: number };
	let hearts = $state<Heart[]>(
		targets.map((_, i) => ({ id: i, x: originX, y: originY, alpha: 0, scale: 0.5 })),
	);"""
new3 = """	type Heart = { id: number; x: number; y: number; alpha: number; scale: number };
	let hearts = $state<Heart[]>(
		targets.map((_, i) => ({ id: i, x: originX, y: originY, alpha: 0, scale: 0.5 })),
	);
	// Cache chaque case ciblee tant que son coeur n'a pas encore atterri -
	// garantit que le WILD n'est JAMAIS visible avant que le coeur ne le
	// "revele" a l'ecran, quelle que soit la donnee deja presente en dessous.
	let maskVisible = $state<boolean[]>(targets.map(() => true));"""
n = content.count(old3)
if n != 1:
    results.append(f"ERREUR (maskVisible) : {n} fois.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (etat maskVisible ajoute)")

old4 = "\t\t\t\t\t\thearts[index].alpha = 0;\n\t\t\t\t\t\tresolve();"
new4 = "\t\t\t\t\t\thearts[index].alpha = 0;\n\t\t\t\t\t\tmaskVisible[index] = false;\n\t\t\t\t\t\tresolve();"
n = content.count(old4)
if n != 1:
    results.append(f"ERREUR (retrait cache a l'atterrissage) : {n} fois.")
else:
    content = content.replace(old4, new4, 1)
    results.append("OK (cache retire exactement a l'atterrissage du coeur)")

old5 = """{#each hearts as heart (heart.id)}
	<Container x={heart.x} y={heart.y} alpha={heart.alpha} scale={heart.scale} zIndex={40}>
		<Sprite key="heartBullet" anchor={0.5} width={HEART_SIZE} height={HEART_SIZE} />
	</Container>
{/each}"""
new5 = """{#each targets as target, i}
	{#if maskVisible[i]}
		<Rectangle
			x={target.x}
			y={target.y}
			anchor={0.5}
			width={SYMBOL_SIZE}
			height={SYMBOL_SIZE}
			backgroundColor={0x1a0a14}
			zIndex={35}
		/>
	{/if}
{/each}
{#each hearts as heart (heart.id)}
	<Container x={heart.x} y={heart.y} alpha={heart.alpha} scale={heart.scale} zIndex={40}>
		<Sprite key="heartBullet" anchor={0.5} width={HEART_SIZE} height={HEART_SIZE} />
	</Container>
{/each}"""
n = content.count(old5)
if n != 1:
    results.append(f"ERREUR (rendu) : {n} fois.")
else:
    content = content.replace(old5, new5, 1)
    results.append("OK (rendu du cache ajoute, au-dessus du plateau mais sous les coeurs)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
