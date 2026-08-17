path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import BannerReveal from './BannerReveal.svelte';"
new_import = old_import + "\nimport SuperlikeHeartThrow from './SuperlikeHeartThrow.svelte';"

old_state = "let bannerX = $state(0);"
new_state = old_state + "\n\tlet revealReelIndex = $state(0);"

old_handler = "bannerX = getSymbolX(emitterEvent.reelIndex);"
new_handler = old_handler + "\n\t\t\trevealReelIndex = emitterEvent.reelIndex;"

old_banner_tag = """oncomplete={() => resolveShow()}
			/>"""
new_banner_tag = """oncomplete={() => resolveShow()}
			/>

			{#if assetKey === 'superlikeReveal'}
				<SuperlikeHeartThrow reelIndex={revealReelIndex} />
			{/if}"""

replacements = [
	(old_import, new_import),
	(old_state, new_state),
	(old_handler, new_handler),
	(old_banner_tag, new_banner_tag),
]

missing = [old for old, new in replacements if old not in content]
if missing:
	print("ERREUR : ancre(s) non trouvee(s), rien modifie :")
	for m in missing:
		print(" -", repr(m))
else:
	for old, new in replacements:
		content = content.replace(old, new, 1)
	with open(path, "w") as f:
		f.write(content)
	print("OK : SuperlikeHeartThrow branche dans SpecialRevealOverlay.svelte.")
