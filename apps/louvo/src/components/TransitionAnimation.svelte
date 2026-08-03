<script lang="ts">
	import { onMount } from 'svelte';

	type Props = {
		oncomplete: () => void;
	};
	const props: Props = $props();

	onMount(() => {
		const timeout = setTimeout(() => props.oncomplete(), 400);
		return () => clearTimeout(timeout);
	});
</script>
