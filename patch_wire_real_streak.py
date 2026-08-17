results = []

# --- 1) typesBookEvent.ts : ajouter streakTier au type ---
path1 = "apps/louvo/src/game/typesBookEvent.ts"
with open(path1, "r") as f:
    c1 = f.read()
old1 = "\tmultiplier: number;\n\tlikes: number;\n\tlikePositions: { reelIndex: number; rowIndex: number }[];"
new1 = "\tmultiplier: number;\n\tlikes: number;\n\tstreakTier: number;\n\tlikePositions: { reelIndex: number; rowIndex: number }[];"
if old1 not in c1:
    results.append("ERREUR typesBookEvent.ts : ancre introuvable.")
else:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, "w") as f:
        f.write(c1)
    results.append("OK typesBookEvent.ts : streakTier ajoute au type.")

# --- 2) stateGame.svelte.ts : ajouter le state ---
path2 = "apps/louvo/src/game/stateGame.svelte.ts"
with open(path2, "r") as f:
    c2 = f.read()
old2 = "\tmultiplierBoard: [] as (MultiplierSymbol | undefined)[][],\n\tscatterCounter: 0,\n});"
new2 = "\tmultiplierBoard: [] as (MultiplierSymbol | undefined)[][],\n\tscatterCounter: 0,\n\tstreakTier: 0,\n\tstreakLikes: 0,\n});"
if old2 not in c2:
    results.append("ERREUR stateGame.svelte.ts : ancre introuvable.")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK stateGame.svelte.ts : streakTier/streakLikes ajoutes.")

# --- 3) bookEventHandlerMap.ts : reset au freeSpinTrigger + mise a jour au superlikeReveal ---
path3 = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path3, "r") as f:
    c3 = f.read()

old3a = "\t\tstateGame.gameType = 'freegame';\n\t\tstateGame.tier = bookEvent.tier ?? 'speed_dating';"
new3a = "\t\tstateGame.gameType = 'freegame';\n\t\tstateGame.tier = bookEvent.tier ?? 'speed_dating';\n\t\tstateGame.streakTier = 0;\n\t\tstateGame.streakLikes = 0;"
if old3a not in c3:
    results.append("ERREUR bookEventHandlerMap.ts (reset) : ancre introuvable.")
else:
    c3 = c3.replace(old3a, new3a, 1)
    results.append("OK bookEventHandlerMap.ts : reset du streak au declenchement d'un bonus.")

old3b = """\t\t\tlikePositions: bookEvent.likePositions,
\t\t});
\t},"""
new3b = """\t\t\tlikePositions: bookEvent.likePositions,
\t\t});
\t\tstateGame.streakTier = bookEvent.streakTier;
\t\tstateGame.streakLikes = bookEvent.likes;
\t},"""
count3b = c3.count(old3b)
if count3b != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts (superlikeReveal) : trouve {count3b} fois (attendu 1).")
else:
    c3 = c3.replace(old3b, new3b, 1)
    results.append("OK bookEventHandlerMap.ts : streakTier/streakLikes mis a jour a chaque superlikeReveal.")

with open(path3, "w") as f:
    f.write(c3)

for r in results:
    print(r)
