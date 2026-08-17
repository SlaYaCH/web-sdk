path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const HEART_SIZE = 40;"
new = "const HEART_SIZE = 28; // meme taille que les coeurs du presentoir"

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : coeurs lances a la meme taille que le presentoir (28px).")
