path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { Sprite } from 'pixi-svelte';"
new_import = "import { Sprite, Rectangle } from 'pixi-svelte';"

old_snippets = """                {#snippet background(sizes)}
                    <Sprite key="progressBarBackground.png" {...sizes} />
                {/snippet}
                {#snippet progress(sizes)}
                    <Sprite key="progressBar.png" {...sizes} />
                {/snippet}
                {#snippet frame(sizes)}
                    <Sprite key="progressBarFrame.png" {...sizes} />
                {/snippet}"""
new_snippets = """                {#snippet background(sizes)}
                    <Rectangle {...sizes} backgroundColor={0x330018} />
                {/snippet}
                {#snippet progress(sizes)}
                    <Rectangle {...sizes} backgroundColor={0xff2d6a} />
                {/snippet}
                {#snippet frame(sizes)}
                    <Rectangle {...sizes} backgroundColor={0x000000} alpha={0} borderColor={0xff2d6a} borderWidth={2} />
                {/snippet}"""

missing = [n for n, o in [("import", old_import), ("snippets", old_snippets)] if o not in content]
if missing:
    print("ERREUR LoadingScreen.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_snippets, new_snippets, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : barre rose simple, sans image.")
