results = []

# --- 1) Game.svelte : ajouter le composant a cote de BoardFrame ---
path1 = "apps/louvo/src/components/Game.svelte"
with open(path1, "r") as f:
    c1 = f.read()

old1a = "import AfterDarkStreakDisplay from './AfterDarkStreakDisplay.svelte';"
new1a = old1a + "\n\timport WinLinesDisplay from './WinLinesDisplay.svelte';"
if old1a not in c1:
    results.append("ERREUR Game.svelte (import) : ancre introuvable.")
else:
    c1 = c1.replace(old1a, new1a, 1)
    results.append("OK Game.svelte (import) : ajoute.")

old1b = "<BoardFrame />"
new1b = "<BoardFrame />\n\t\t\t\t<WinLinesDisplay />"
count1b = c1.count(old1b)
if count1b != 1:
    results.append(f"ERREUR Game.svelte (usage) : trouve {count1b} fois (attendu 1).")
else:
    c1 = c1.replace(old1b, new1b, 1)
    results.append("OK Game.svelte (usage) : WinLinesDisplay ajoute apres BoardFrame.")

with open(path1, "w") as f:
    f.write(c1)

# --- 2) bookEventHandlerMap.ts : winInfo diffuse winLinesShow et ATTEND la fin ---
path2 = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path2, "r") as f:
    c2 = f.read()

old2 = """\twinInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
\t\teventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
\t\tawait sequence(bookEvent.wins, async (win) => {
\t\t\tawait animateSymbols({ positions: win.positions });
\t\t});
\t},"""
new2 = """\twinInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
\t\teventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
\t\tawait sequence(bookEvent.wins, async (win) => {
\t\t\tawait animateSymbols({ positions: win.positions });
\t\t});
\t\tif (bookEvent.wins.length > 0) {
\t\t\teventEmitter.broadcast({ type: 'winLinesShow', wins: bookEvent.wins });
\t\t\t// Duree totale de l'animation d'une ligne (voir WinLineReveal.svelte) :
\t\t\t// 120 (apparition) + 700 (maintien) + 150 (ligne disparait) + 300 (attente) + 250 (montant disparait)
\t\t\tawait new Promise((r) => setTimeout(r, 120 + 700 + 150 + 300 + 250));
\t\t}
\t},"""

count2 = c2.count(old2)
if count2 != 1:
    results.append(f"ERREUR bookEventHandlerMap.ts : trouve {count2} fois (attendu 1).")
else:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, "w") as f:
        f.write(c2)
    results.append("OK bookEventHandlerMap.ts : winLinesShow diffuse, attend la fin de l'animation avant de continuer.")

for r in results:
    print(r)
