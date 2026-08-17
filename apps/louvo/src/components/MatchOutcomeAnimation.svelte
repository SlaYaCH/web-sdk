<script lang="ts">
	import { onMount } from 'svelte';
	import { SpriteSheet } from 'pixi-svelte';

	type Props = {
		biggerWon: boolean;
		width: number;
		height: number;
	};
	const props: Props = $props();

	let play = $state(false);

	onMount(() => {
		play = true;
	});
</script>

<SpriteSheet
	key={props.biggerWon ? 'matchRevealKiss' : 'matchRevealExit'}
	{play}
	loop={false}
	animationSpeed={10 / 60}
	anchor={0.5}
	width={props.width}
	height={props.height}
/>
