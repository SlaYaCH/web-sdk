path = "apps/louvo/src/components/SpecialRevealOverlay.svelte"
with open(path, "r") as f:
    content = f.read()

old_state = "let bannerX = $state(0);"
new_state = "let bannerX = $state(0);\n\tlet forceClose = $state(false);"

old_subscribe = """	context.eventEmitter.subscribeOnMount({
		specialRevealShow: async (emitterEvent) => {
			assetKey = emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal';"""
new_subscribe = """	context.eventEmitter.subscribeOnMount({
		spinStart: () => {
			if (show) forceClose = true;
		},
		specialRevealShow: async (emitterEvent) => {
			forceClose = false;
			assetKey = emitterEvent.symbol === 'M' ? 'matchReveal' : 'superlikeReveal';"""

old_holdms = "holdMs={999999}"
new_holdms = "holdMs={15000}\n\t\t\t\tforceClose={forceClose}"

missing = [n for n, o in [("state", old_state), ("subscribe", old_subscribe), ("holdms", old_holdms)] if o not in content]
if missing:
    print("ERREUR : ancre(s) non trouvee(s) :", missing)
else:
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_subscribe, new_subscribe, 1)
    content = content.replace(old_holdms, new_holdms, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SpecialRevealOverlay.svelte se ferme desormais sur spinStart (15s de securite max).")
