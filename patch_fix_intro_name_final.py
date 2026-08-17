path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = "src: new URL('../../assets/sprites/screens/intro_screen.png', import.meta.url).href,"
new = "src: new URL('../../assets/sprites/screens/louvo_intro_screen.png', import.meta.url).href,"

count = content.count(old)
if count == 0:
    print("ERREUR : ancre introuvable.")
elif count > 1:
    print(f"ERREUR : ancre trouvee {count} fois (ambigue), verification manuelle necessaire.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : pointe vers louvo_intro_screen.png.")
