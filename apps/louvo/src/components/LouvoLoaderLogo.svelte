<script lang="ts">
	import { LoaderBase } from 'components-shared';
	type Props = {
		src: string;
		oncomplete?: () => void;
	};
	const props: Props = $props();
</script>

<LoaderBase maxWidth={280} backgroundColor={'#000000'} timeout={800} src={props.src} oncomplete={props.oncomplete} />
