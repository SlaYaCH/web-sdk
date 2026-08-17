path = "packages/components-ui-html/src/components/Modals.svelte"
with open(path, "r") as f:
    content = f.read()

# 1) Ajouter les props optionnelles juste apres "version: Snippet;" (ligne unique, sans risque d'espaces)
marker_props = "version: Snippet;"
count_props = content.count(marker_props)
if count_props != 1:
    print(f"ERREUR : 'version: Snippet;' trouve {count_props} fois (attendu 1) - arret sans modification.")
else:
    idx = content.index(marker_props) + len(marker_props)
    content = content[:idx] + "\n\tgameRules?: Snippet;\n\tpayTable?: Snippet;" + content[idx:]

    # 2) Cibler UNIQUEMENT le bloc ModalGameRules (apres <ModalGameRules>, avant </ModalGameRules>)
    start_tag = "<ModalGameRules>"
    end_tag = "</ModalGameRules>"
    start_idx = content.index(start_tag) + len(start_tag)
    end_idx = content.index(end_tag)
    inner = content[start_idx:end_idx]
    if "props.version()" not in inner:
        print("ERREUR : contenu interne de ModalGameRules inattendu, rien touche.")
    else:
        new_inner = inner.replace(
            "{@render props.version()}",
            "{#if props.gameRules}{@render props.gameRules()}{:else}{@render props.version()}{/if}",
        )
        content = content[:start_idx] + new_inner + content[end_idx:]

        with open(path, "w") as f:
            f.write(content)
        print("OK : props ajoutees et ModalGameRules affiche desormais props.gameRules en priorite.")
