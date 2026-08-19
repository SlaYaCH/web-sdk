path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old = """		<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
		{#if bonusActive}
			<Rectangle anchor={0.5} width={90} height={90} alpha={0} borderColor={0xffffff} borderWidth={4} />
		{/if}"""
new = """		<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
		{#if bonusActive}
			<Rectangle anchor={0.5} width={90} height={90} alpha={0} borderColor={0xffffff} borderWidth={4} />
			<Rectangle
				anchor={{ x: 0.5, y: 0 }}
				y={38}
				width={78}
				height={26}
				backgroundColor={0xff2d6a}
				borderColor={0xffffff}
				borderWidth={2}
			/>
			<Text
				anchor={{ x: 0.5, y: 0 }}
				y={41}
				text="OFF"
				style={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 16, fill: 0xffffff }}
			/>
		{/if}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : badge 'OFF' cliquable ajoute par-dessus l'icone bonus quand un mode est actif.")
