path = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path, "r") as f:
    content = f.read()

old = "\t\tstateGame.gameType = 'freegame';\n\t\tstateGame.tier = bookEvent.tier ?? 'speed_dating';\n"
new = "\t\tstateGame.gameType = 'freegame';\n"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : doublon retire, tier n'est plus defini qu'une fois (plus tot, avant l'ecran d'annonce).")
