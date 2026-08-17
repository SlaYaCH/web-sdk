<script lang="ts">
    import { Sprite, Rectangle } from 'pixi-svelte';
    import { FadeContainer, LoadingProgress } from 'components-pixi';
    import { MainContainer } from 'components-layout';

    import { getContext } from '../game/context';
    import TransitionAnimation from './TransitionAnimation.svelte';
    import PressToContinue from './PressToContinue.svelte';

    type Props = {
        onloaded: () => void;
    };

    const props: Props = $props();
    const context = getContext();

    let loadingType = $state<'start' | 'transition'>('start');
</script>

<FadeContainer show={loadingType === 'start'}>
    <MainContainer>
        {#if !context.stateApp.loaded}
            <LoadingProgress
                x={context.stateLayoutDerived.mainLayout().width * 0.5009}
                y={context.stateLayoutDerived.mainLayout().height * 0.7502}
                width={context.stateLayoutDerived.mainLayout().width * 0.3343}
                height={context.stateLayoutDerived.mainLayout().height * 0.0524}
            >
                {#snippet background(sizes)}
                    <Rectangle {...sizes} backgroundColor={0x330018} />
                {/snippet}
                {#snippet progress(sizes)}
                    <Rectangle {...sizes} backgroundColor={0xff2d6a} />
                {/snippet}
                {#snippet frame(sizes)}
                    <Rectangle {...sizes} backgroundColor={0x000000} alpha={0} />
                {/snippet}
            </LoadingProgress>
        {/if}
        <Sprite
            key="loadingScreen"
            x={context.stateLayoutDerived.mainLayout().width * 0.5}
            y={context.stateLayoutDerived.mainLayout().height * 0.5}
            anchor={0.5}
            width={context.stateLayoutDerived.mainLayout().width}
            height={context.stateLayoutDerived.mainLayout().height}
        />
    </MainContainer>
</FadeContainer>

<FadeContainer show={loadingType === 'start' && context.stateApp.loaded}>
    <PressToContinue onpress={() => (loadingType = 'transition')} />
</FadeContainer>

<FadeContainer show={loadingType === 'transition'}>
    <TransitionAnimation oncomplete={props.onloaded} />
</FadeContainer>
