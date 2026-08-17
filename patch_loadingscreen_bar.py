path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { Sprite } from 'pixi-svelte';\nimport { FadeContainer } from 'components-pixi';"
new_import = "import { Sprite } from 'pixi-svelte';\nimport { FadeContainer, LoadingProgress } from 'components-pixi';"

old_block = """        <Sprite
            key="loadingScreen"
            x={context.stateLayoutDerived.mainLayout().width * 0.5}
            y={context.stateLayoutDerived.mainLayout().height * 0.5}
            anchor={0.5}
            width={context.stateLayoutDerived.mainLayout().width}
            height={context.stateLayoutDerived.mainLayout().height}
        />
    </MainContainer>
</FadeContainer>"""
new_block = """        <Sprite
            key="loadingScreen"
            x={context.stateLayoutDerived.mainLayout().width * 0.5}
            y={context.stateLayoutDerived.mainLayout().height * 0.5}
            anchor={0.5}
            width={context.stateLayoutDerived.mainLayout().width}
            height={context.stateLayoutDerived.mainLayout().height}
        />
        {#if !context.stateApp.loaded}
            <LoadingProgress
                x={context.stateLayoutDerived.mainLayout().width * 0.5}
                y={context.stateLayoutDerived.mainLayout().height * 0.82}
                width={492 * 0.6}
                height={87 * 0.6}
            >
                {#snippet background(sizes)}
                    <Sprite key="progressBarBackground.png" {...sizes} />
                {/snippet}
                {#snippet progress(sizes)}
                    <Sprite key="progressBar.png" {...sizes} />
                {/snippet}
                {#snippet frame(sizes)}
                    <Sprite key="progressBarFrame.png" {...sizes} />
                {/snippet}
            </LoadingProgress>
        {/if}
    </MainContainer>
</FadeContainer>"""

missing = [n for n, o in [("import", old_import), ("block", old_block)] if o not in content]
if missing:
    print("ERREUR LoadingScreen.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : barre de progression animee ajoutee (branchee sur le vrai pourcentage de chargement).")
