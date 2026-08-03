<script lang="ts">
	// Louvo : pas d'asset "coins" (spritesheet de pièces animées) pour
	// l'instant - effet neutralisé en attendant, plutôt que de planter
	// sur une clé manquante.
	type Props = {
		emit?: boolean;
		levelAlias?: string;
	};
	const props: Props = $props();
</script>
