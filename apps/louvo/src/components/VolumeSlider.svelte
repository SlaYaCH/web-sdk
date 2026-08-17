<script lang="ts">
	import { Container, Rectangle } from 'pixi-svelte';

	type Props = {
		value: number; // 0-100
		width: number;
		onchange: (value: number) => void;
	};
	const props: Props = $props();

	// ============================================================
	// REGLAGES RAPIDES
	// ============================================================
	const TRACK_HEIGHT = 8;
	const HANDLE_SIZE = 26;

	let isDragging = $state(false);

	const clamp = (v: number) => Math.max(0, Math.min(100, v));

	const valueFromLocalX = (localX: number) => {
		const t = (localX + props.width / 2) / props.width;
		return clamp(Math.round(t * 100));
	};

	const handleX = () => (props.value / 100) * props.width - props.width / 2;

	const updateFromEvent = (e: any) => {
		const local = e.getLocalPosition(e.currentTarget);
		props.onchange(valueFromLocalX(local.x));
	};

	const onDown = (e: any) => {
		isDragging = true;
		updateFromEvent(e);
	};
	const onMove = (e: any) => {
		if (!isDragging) return;
		updateFromEvent(e);
	};
	const onUp = () => {
		isDragging = false;
	};
</script>

<Container
	eventMode="static"
	cursor="pointer"
	onpointerdown={onDown}
	onglobalpointermove={onMove}
	onpointerup={onUp}
	onpointerupoutside={onUp}
>
	<Rectangle
		anchor={0.5}
		width={props.width}
		height={TRACK_HEIGHT}
		backgroundColor={0x330018}
		borderColor={0xff2d6a}
		borderWidth={1}
	/>
	<Rectangle
		x={-props.width / 2}
		anchor={{ x: 0, y: 0.5 }}
		width={Math.max(0, (props.value / 100) * props.width)}
		height={TRACK_HEIGHT}
		backgroundColor={0xff2d6a}
	/>
	<Rectangle
		x={handleX()}
		anchor={0.5}
		width={HANDLE_SIZE}
		height={HANDLE_SIZE}
		backgroundColor={0xffffff}
		borderColor={0xff2d6a}
		borderWidth={3}
	/>
</Container>
