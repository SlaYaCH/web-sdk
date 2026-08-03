<script lang="ts">
	import { MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { Text, REM } from 'pixi-svelte';
	import { getContext } from '../game/context';
	type Props = {
		onpress: () => void;
	};
	const props: Props = $props();
	const context = getContext();
</script>
<MainContainer alignVertical="bottom">
	<Text
		anchor={{ x: 0.5, y: 1 }}
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height - 40}
		text="TAP TO CONTINUE"
		style={{
			fontFamily: 'proxima-nova',
			fontSize: REM * 1.5,
			fontWeight: '600',
			fill: 0xffffff,
		}}
	/>
</MainContainer>
<OnHotkey hotkey="Space" onpress={() => props.onpress()} />
<OnPressFullScreen onpress={() => props.onpress()} />
