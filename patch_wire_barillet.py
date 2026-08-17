path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import { SYMBOL_WIDTH, SYMBOL_HEIGHT, BOARD_DIMENSIONS } from '../game/constants';"
new_import = old_import + "\n\timport SuperlikeBarillet from './SuperlikeBarillet.svelte';"

old_tag = "<Sprite anchor={0.5} key={props.assetKey} width={bannerWidth} height={bannerHeight} />"
new_tag = old_tag + "\n\n\t{#if props.assetKey === 'superlikeReveal'}\n\t\t<SuperlikeBarillet />\n\t{/if}"

if old_import not in content or old_tag not in content:
    print("ERREUR : ancre(s) non trouvee(s), rien modifie.")
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_tag, new_tag, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : SuperlikeBarillet branche dans BannerReveal.svelte.")
