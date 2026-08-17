<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	type Props = {
		cardKey: string;
		width: number;
		height: number;
		achieved?: boolean;
	};

	const props: Props = $props();
</script>

<Sprite
	key={props.cardKey}
	anchor={0.5}
	width={props.width}
	height={props.height}
	tint={props.achieved ? 0x666666 : 0xffffff}
	alpha={props.achieved ? 0.45 : 1}
/>
