<script lang="ts">
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { stateSound, stateBet, stateBetDerived, stateModal, stateUi } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();

	const PANEL_WIDTH = 380;
	const PANEL_HEIGHT = 480;
	const ROW_WIDTH = PANEL_WIDTH - 40;
	const ROW_HEIGHT = 55;
	const ROW_GAP = 70;

	const onSound = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateSound.volumeValueMaster = stateSound.volumeValueMaster === 0 ? 50 : 0;
	};
	// Musique : pas de canal separe dans ce moteur - meme bascule que le son maitre
	const onMusic = () => onSound();

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

	const soundLabel = $derived(stateSound.volumeValueMaster === 0 ? 'SON : COUPÉ' : 'SON : ACTIF');
	const turboLabel = $derived(stateBet.isTurbo ? 'TURBO : ACTIF' : 'TURBO : COUPÉ');
	const superTurboLabel = $derived(stateBet.isSuperTurbo ? 'SUPER TURBO : ACTIF' : 'SUPER TURBO : COUPÉ');

	const ROWS = $derived([
		{ label: soundLabel, onpress: onSound },
		{ label: 'MUSIQUE', onpress: onMusic },
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

	{#each ROWS as row, i}
		<Container
			y={-PANEL_HEIGHT / 2 + 55 + i * ROW_GAP}
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
