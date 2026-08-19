path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = """	type Heart = { id: number; x: number; y: number; alpha: number; scale: number };
	let hearts = $state<Heart[]>(
		targets.map((_, i) => ({ id: i, x: originX, y: originY, alpha: 0, scale: 0.5 })),
	);"""
new1 = """	type Heart = { id: number; x: number; y: number; alpha: number; scale: number };
	let hearts = $state<Heart[]>(
		targets.map((_, i) => ({ id: i, x: originX, y: originY, alpha: 0, scale: 0.5 })),
	);
	// Cache chaque case ciblee tant que son coeur n'a pas encore atterri -
	// garantit que le WILD n'est JAMAIS visible avant que le coeur ne le
	// "revele" a l'ecran, quelle que soit la donnee deja presente en dessous.
	let maskVisible = $state<boolean[]>(targets.map(() => true));"""
n = content.count(old1)
if n != 1:
    results.append(f"ERREUR (maskVisible) : {n} fois.")
else:
    content = content.replace(old1, new1, 1)
    results.append("OK (etat maskVisible ajoute)")

old2 = """					context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode', forcePlay: true });
					// Le coeur disparait immediatement : le vrai symbole WILD
					// prend le relais visuellement a cet instant precis.
					hearts[index].alpha = 0;
					resolve();"""
new2 = """					context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode', forcePlay: true });
					// Le coeur disparait immediatement : le vrai symbole WILD
					// prend le relais visuellement a cet instant precis.
					hearts[index].alpha = 0;
					maskVisible[index] = false;
					resolve();"""
n = content.count(old2)
if n != 1:
    results.append(f"ERREUR (retrait cache) : {n} fois.")
else:
    content = content.replace(old2, new2, 1)
    results.append("OK (cache retire exactement a l'atterrissage du coeur)")

old3 = """{#each hearts as heart (heart.id)}
	<Container x={heart.x} y={heart.y} alpha={heart.alpha} scale={heart.scale}>
		<Sprite key="heartBullet" anchor={0.5} width={HEART_SIZE} height={HEART_SIZE} />
	</Container>
{/each}"""
new3 = """{#each targets as target, i}
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
n = content.count(old3)
if n != 1:
    results.append(f"ERREUR (rendu) : {n} fois.")
else:
    content = content.replace(old3, new3, 1)
    results.append("OK (rendu du cache ajoute + zIndex sur les coeurs)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
