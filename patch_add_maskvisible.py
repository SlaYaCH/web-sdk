path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = "\t);\n{#each targets as target, i}"
new = "\t);\n\t// Cache chaque case ciblee tant que son coeur n'a pas encore atterri -\n\t// garantit que le WILD n'est JAMAIS visible avant que le coeur ne le\n\t// \"revele\" a l'ecran, quelle que soit la donnee deja presente en dessous.\n\tlet maskVisible = $state<boolean[]>(targets.map(() => true));\n</script>\n{#each targets as target, i}"

# Cette ancre n'est pas fiable (elle contient </script> qui n'apparait qu'une fois,
# donc on cherche juste avant la fermeture du script a la place.
old2 = "\t});\n</script>\n{#each targets as target, i}"
new2 = "\t});\n\t// Cache chaque case ciblee tant que son coeur n'a pas encore atterri -\n\t// garantit que le WILD n'est JAMAIS visible avant que le coeur ne le\n\t// \"revele\" a l'ecran, quelle que soit la donnee deja presente en dessous.\n\tlet maskVisible = $state<boolean[]>(targets.map(() => true));\n</script>\n{#each targets as target, i}"

count2 = content.count(old2)
if count2 != 1:
    print(f"ERREUR : trouve {count2} fois (attendu 1).")
else:
    content = content.replace(old2, new2, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : maskVisible ajoute juste avant la fermeture du script.")
