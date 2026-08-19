path = "apps/louvo/src/game/context.ts"
with open(path, "r") as f:
    content = f.read()

results = []

old1 = "\tMATCH_BOOST: LOUVO_BET_MODE_SHAPE('MATCH_BOOST', 3.0),\n\tMATCH_FRENZY: LOUVO_BET_MODE_SHAPE('MATCH_FRENZY', 60.0),\n\tLIKE_STORM: LOUVO_BET_MODE_SHAPE('LIKE_STORM', 60.0),"
new1 = "\tMATCH_BOOST: { ...LOUVO_BET_MODE_SHAPE('MATCH_BOOST', 3.0), type: 'activate' as const },\n\tMATCH_FRENZY: { ...LOUVO_BET_MODE_SHAPE('MATCH_FRENZY', 60.0), type: 'activate' as const },\n\tLIKE_STORM: { ...LOUVO_BET_MODE_SHAPE('LIKE_STORM', 60.0), type: 'activate' as const },"

count = content.count(old1)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old1, new1, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : MATCH_BOOST/MATCH_FRENZY/LIKE_STORM passent en type 'activate' - le bouton bonus existant les rendra desactivables automatiquement.")
