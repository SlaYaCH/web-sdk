path = "apps/louvo/src/components/SuperlikeBarilletDisplay.svelte"
with open(path, "r") as f:
    content = f.read()

old_hub = "const HUB_Y = 154;"
new_hub = "const HUB_Y = 152.5;"

old_size = "const HEART_SIZE = 58;"
new_size = "const HEART_SIZE = 50;"

old_sync = "animate(200, 300 + i * 80, (t) => {"
new_sync = "animate(200, 300 + i * 550, (t) => {"

missing = [n for n, o in [("hub", old_hub), ("size", old_size), ("sync", old_sync)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_hub, new_hub, 1)
    content = content.replace(old_size, new_size, 1)
    content = content.replace(old_sync, new_sync, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : HUB_Y=152.5, coeurs a 50px, synchro du presentoir alignee sur le lancer sequentiel (550ms/coeur).")
