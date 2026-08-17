path = "apps/louvo/src/components/AfterDarkHeartTally.svelte"
with open(path, "r") as f:
    content = f.read()

replacements = [
    ("const REMOVE_STAGGER_MS = 150;", "const REMOVE_STAGGER_MS = 550;"),
    ("const REMOVE_DURATION_MS = 220;", "const REMOVE_DURATION_MS = 400;"),
]

missing = []
for old, new in replacements:
    if content.count(old) != 1:
        missing.append(old)
    else:
        content = content.replace(old, new, 1)

if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    with open(path, "w") as f:
        f.write(content)
    print("OK : rythme cale sur SuperlikeHeartThrow (550ms entre chaque coeur, comme le vrai lancer).")
