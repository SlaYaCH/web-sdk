path = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old = "const TITLE_Y_FRAC = 0.2976;"
new = "const TITLE_Y_FRAC = 0.335;"

if old not in content:
    print("ERREUR LouvoIntroScreen.svelte : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : titres descendus sous le cadre du haut.")
