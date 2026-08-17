path = "apps/louvo/src/components/SymbolSprite.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { onMount } from 'svelte';"
new_import = "import { onMount } from 'svelte';\n\timport { stateGame } from '../game/stateGame.svelte';"

old_sprite = """<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_WIDTH * props.symbolInfo.sizeRatios.width}
	height={SYMBOL_HEIGHT * props.symbolInfo.sizeRatios.height}
	zIndex={props.zIndex}
/>"""
new_sprite = """<script lang="ts">
	// 2% plus grand en After Dark (cadre plus grand que la base)
	const AFTER_DARK_SIZE_SCALE = 1.02;
	const sizeScale = $derived(stateGame.tier === 'after_dark' ? AFTER_DARK_SIZE_SCALE : 1);
</script>

<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_WIDTH * props.symbolInfo.sizeRatios.width * sizeScale}
	height={SYMBOL_HEIGHT * props.symbolInfo.sizeRatios.height * sizeScale}
	zIndex={props.zIndex}
/>"""

missing = [n for n, o in [("import", old_import), ("sprite", old_sprite)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_sprite, new_sprite, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : symboles 2% plus grands en After Dark.")
