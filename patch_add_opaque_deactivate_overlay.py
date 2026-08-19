path = "apps/louvo/src/components/LouvoBottomBar.svelte"
with open(path, "r") as f:
    content = f.read()

old = """\t\t<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
\t\t{#if bonusActive}
\t\t\t<Rectangle anchor={0.5} width={90} height={90} alpha={0} borderColor={0xffffff} borderWidth={4} />
\t\t{/if}"""
new = """\t\t<Sprite key="uiBonusIcon" anchor={0.5} width={90} height={90} />
\t\t{#if bonusActive}
\t\t\t<Rectangle anchor={0.5} width={90} height={90} backgroundColor={0x1a0a14} borderColor={0xff2d6a} borderWidth={4} />
\t\t\t<Text
\t\t\t\tanchor={0.5}
\t\t\t\ttext="OFF"
\t\t\t\tstyle={{ fontFamily: 'proxima-nova', fontWeight: '700', fontSize: 24, fill: 0xffffff }}
\t\t\t/>
\t\t{/if}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : icone bonus entierement recouverte d'un fond opaque + texte OFF quand un mode est actif.")
