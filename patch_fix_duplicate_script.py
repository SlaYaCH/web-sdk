path = "apps/louvo/src/components/SymbolSprite.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	$effect(() => {
		props.symbolInfo;
		props.oncomplete?.();
	});
</script>
<script lang="ts">
	// 2% plus grand en After Dark (cadre plus grand que la base)
	const AFTER_DARK_SIZE_SCALE = 1.02;
	const sizeScale = $derived(stateGame.tier === 'after_dark' ? AFTER_DARK_SIZE_SCALE : 1);
</script>"""

new = """	$effect(() => {
		props.symbolInfo;
		props.oncomplete?.();
	});

	// 2% plus grand en After Dark (cadre plus grand que la base)
	const AFTER_DARK_SIZE_SCALE = 1.02;
	const sizeScale = $derived(stateGame.tier === 'after_dark' ? AFTER_DARK_SIZE_SCALE : 1);
</script>"""

if old not in content:
    print("ERREUR : ancre introuvable - le fichier a peut-etre deja ete corrige ou modifie autrement.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les deux blocs script fusionnes en un seul.")

echo_check = "<script lang=\"ts\">" in content and content.count("<script lang=\"ts\">") == 1
print("Nombre de blocs <script lang=\"ts\"> restants :", content.count('<script lang="ts">'))
