path = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path, "r") as f:
    content = f.read()

old = """\twinInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
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

new = """\twinInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
\t\teventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
\t\tif (bookEvent.wins.length > 0) {
\t\t\t// Affichee tout de suite (pas apres la surbrillance des symboles),
\t\t\t// directement quand le 5eme rouleau vient de s'arreter.
\t\t\teventEmitter.broadcast({ type: 'winLinesShow', wins: bookEvent.wins });
\t\t}
\t\tawait sequence(bookEvent.wins, async (win) => {
\t\t\tawait animateSymbols({ positions: win.positions });
\t\t});
\t\tif (bookEvent.wins.length > 0) {
\t\t\t// Duree totale de l'animation d'une ligne (voir WinLineReveal.svelte) :
\t\t\t// 120 (apparition) + 700 (maintien) + 150 (ligne disparait) + 300 (attente) + 250 (montant disparait)
\t\t\tawait new Promise((r) => setTimeout(r, 120 + 700 + 150 + 300 + 250));
\t\t}
\t},"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1) - verification manuelle necessaire.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : la ligne s'affiche desormais immediatement, en parallele de la surbrillance des symboles (plus d'attente).")
