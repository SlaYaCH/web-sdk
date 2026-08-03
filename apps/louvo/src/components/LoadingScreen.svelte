<script lang="ts">
    import { Sprite } from 'pixi-svelte';
    import { FadeContainer } from 'components-pixi';
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
