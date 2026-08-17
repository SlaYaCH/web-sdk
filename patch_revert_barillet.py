path = "apps/louvo/src/components/BannerReveal.svelte"
with open(path, "r") as f:
    content = f.read()

import_line = "\n\timport SuperlikeBarillet from './SuperlikeBarillet.svelte';"
usage_block = "\n\n\t{#if props.assetKey === 'superlikeReveal'}\n\t\t<SuperlikeBarillet />\n\t{/if}"

changed = False
if import_line in content:
    content = content.replace(import_line, "")
    changed = True
if usage_block in content:
    content = content.replace(usage_block, "")
    changed = True

if changed:
    with open(path, "w") as f:
        f.write(content)
    print("OK : BannerReveal.svelte revenu a son etat d'origine.")
else:
    print("ATTENTION : rien trouve a retirer (deja revert ou fichier different).")
