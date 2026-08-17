<script lang="ts">
	import { Sprite, Text } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../game/context';
	import PressToContinue from './PressToContinue.svelte';

	type Props = {
		onpress: () => void;
	};
	const props: Props = $props();
	const context = getContext();

	// Mesures reelles sur intro_screen.png (1672x941) : 3 panneaux,
	// zone titre au-dessus de l'illustration, zone texte en dessous.
	const PANEL_X_FRACS = [0.265, 0.4993, 0.7196];
	const TITLE_Y_FRAC = 0.371;
	const BODY_Y_FRAC = 0.7725;
	const PANEL_TEXT_WIDTH_FRAC = 0.179;

	const PANELS = [
		{
			title: 'MATCH & SUPER LIKE',
			body: 'The MATCH and SUPER LIKE reels bring multipliers and a rain of wilds!',
		},
		{
			title: 'TWO BONUSES THAT MATCH',
			body: 'Face off in SPEED DATING and AFTER DARK, two explosive free spin rounds to turn up the heat!',
		},
		{
			title: 'MAXIMUM WIN',
			body: 'Land the ultimate crush: a win that can climb up to 15,000x your bet!',
		},
	];

	const mainW = $derived(context.stateLayoutDerived.mainLayout().width);
	const mainH = $derived(context.stateLayoutDerived.mainLayout().height);
</script>

<MainContainer>
	<Sprite
		key="louvoIntroScreen"
		x={mainW * 0.5}
		y={mainH * 0.5}
		anchor={0.5}
		width={mainW}
		height={mainH}
	/>

	{#each PANELS as panel, i}
		<Text
			anchor={0.5}
			x={mainW * PANEL_X_FRACS[i]}
			y={mainH * TITLE_Y_FRAC}
			text={panel.title}
			style={{
				fontFamily: 'proxima-nova',
				fontWeight: '600',
				fontSize: 20,
				fill: 0xff2d6a,
				align: 'center',
				wordWrap: true,
				wordWrapWidth: mainW * PANEL_TEXT_WIDTH_FRAC,
			}}
		/>
		<Text
			anchor={0.5}
			x={mainW * PANEL_X_FRACS[i]}
			y={mainH * BODY_Y_FRAC}
			text={panel.body}
			style={{
				fontFamily: 'proxima-nova',
				fontWeight: '600',
				fontSize: 14,
				fill: 0xff2d6a,
				align: 'center',
				wordWrap: true,
				wordWrapWidth: mainW * PANEL_TEXT_WIDTH_FRAC,
			}}
		/>
	{/each}
</MainContainer>
<PressToContinue onpress={props.onpress} />
