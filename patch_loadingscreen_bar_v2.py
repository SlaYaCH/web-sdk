path = "apps/louvo/src/components/LoadingScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = """import { Sprite } from 'pixi-svelte';
import { FadeContainer } from 'components-pixi';"""
new_import = """import { Sprite } from 'pixi-svelte';
import { FadeContainer, LoadingProgress } from 'components-pixi';"""

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
        <!-- Mesures reelles sur loading_screen.png (1672x941) : la barre vide
             encadree de coeurs est a x:475-1005, y:608-655 -->
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
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : barre de progression animee, calee precisement sur l'emplacement dessine dans votre image.")
