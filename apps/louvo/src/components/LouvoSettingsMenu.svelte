<script lang="ts">
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { stateSound, stateBet, stateBetDerived, stateModal, stateUi } from 'state-shared';

	import { getContext } from '../game/context';
	import VolumeSlider from './VolumeSlider.svelte';

	const context = getContext();

	const PANEL_WIDTH = 380;
	const PANEL_HEIGHT = 560;
	const ROW_WIDTH = PANEL_WIDTH - 40;
	const ROW_HEIGHT = 55;
	const ROW_GAP = 70;
	const SLIDER_ROW_GAP = 90;

	// Turbo / Super Turbo : un seul niveau de turbo existe dans ce moteur
	const onTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const next = !stateBet.isTurbo;
		stateBetDerived.updateIsTurbo(next, { persistent: true });
		if (!next) stateBet.isSuperTurbo = false;
	};
	const onSuperTurbo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const next2 = !stateBet.isSuperTurbo;
		stateBet.isSuperTurbo = next2;
		if (next2) stateBetDerived.updateIsTurbo(true, { persistent: true });
	};

	const onInfo = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateModal.modal = { name: 'gameRules' };
	};

	// Accueil : pas de mecanisme de sortie/lobby existant - ferme le panneau
	const onHome = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateUi.menuOpen = false;
	};

	const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');
	const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO : ACTIF' : 'SUPER TURBO : COUPÉ');

	const BUTTON_ROWS = $derived([
		{ label: turboLabel, onpress: onTurbo },
		{ label: superTurboLabel, onpress: onSuperTurbo },
		{ label: 'INFO / RÈGLES', onpress: onInfo },
		{ label: 'FERMER', onpress: onHome },
	]);
</script>

<Container>
	<Rectangle
		anchor={0.5}
		width={PANEL_WIDTH}
		height={PANEL_HEIGHT}
		backgroundColor={0x1a0a14}
		borderColor={0xff2d6a}
		borderWidth={4}
	/>

	<!-- Curseur MUSIQUE -->
	<Container y={-PANEL_HEIGHT / 2 + 50}>
		<Text
			y={-14}
			anchor={{ x: 0.5, y: 1 }}
			text={`MUSIQUE : ${Math.round(stateSound.volumeValueMusic)}%`}
			style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 22, fill: 0xffffff }}
		/>
		<Container y={20}>
			<VolumeSlider
				value={stateSound.volumeValueMusic}
				width={ROW_WIDTH}
				onchange={(v) => (stateSound.volumeValueMusic = v)}
			/>
		</Container>
	</Container>

	<!-- Curseur SON -->
	<Container y={-PANEL_HEIGHT / 2 + 50 + SLIDER_ROW_GAP}>
		<Text
			y={-14}
			anchor={{ x: 0.5, y: 1 }}
			text={`SON : ${Math.round(stateSound.volumeValueSoundEffect)}%`}
			style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 22, fill: 0xffffff }}
		/>
		<Container y={20}>
			<VolumeSlider
				value={stateSound.volumeValueSoundEffect}
				width={ROW_WIDTH}
				onchange={(v) => (stateSound.volumeValueSoundEffect = v)}
			/>
		</Container>
	</Container>

	{#each BUTTON_ROWS as row, i}
		<Container
			y={-PANEL_HEIGHT / 2 + 50 + SLIDER_ROW_GAP * 2 + 20 + i * ROW_GAP}
			eventMode="static"
			cursor="pointer"
			onpointerup={row.onpress}
		>
			<Rectangle
				anchor={0.5}
				width={ROW_WIDTH}
				height={ROW_HEIGHT}
				backgroundColor={0x330018}
				borderColor={0xff2d6a}
				borderWidth={2}
			/>
			<Text
				anchor={0.5}
				text={row.label}
				style={{ fontFamily: 'proxima-nova', fontWeight: '600', fontSize: 24, fill: 0xffffff }}
			/>
		</Container>
	{/each}
</Container>
