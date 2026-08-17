path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

# Import : recherche sur UNE SEULE ligne cette fois, pour eviter tout probleme d'espaces invisibles
old_import = "import { FadeContainer } from 'components-pixi';"
new_import = "import { FadeContainer, LoadingProgress } from 'components-pixi';"

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
                x={context.stateLayoutDerived.mainLayout().width * 0.4426}
                y={context.stateLayoutDerived.mainLayout().height * 0.6462}
                width={context.stateLayoutDerived.mainLayout().width * 0.317}
                height={context.stateLayoutDerived.mainLayout().height * 0.05}
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
    for n, o in [("import", old_import), ("block", old_block)]:
        if o not in content:
            print(f"--- anchor '{n}' recherchee (premiere ligne) : {repr(o.splitlines()[0])}")
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : barre de progression animee ajoutee.")
