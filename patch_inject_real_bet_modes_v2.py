path = "apps/louvo/src/game/context.ts"
with open(path, "r") as f:
    content = f.read()

results = []

old_a = "import { i18nDerived } from '../i18n/i18nDerived';\n"
new_a = """import { i18nDerived } from '../i18n/i18nDerived';
import { stateMeta } from 'state-shared';

const LOUVO_BET_MODE_SHAPE = (mode: string, costMultiplier: number) => ({
	mode,
	costMultiplier,
	type: 'buy' as const,
	parent: '',
	children: '',
	assets: { icon: '', dialogImage: '', dialogVolatility: '', volatility: '', button: '' },
	text: { title: '', dialog: '', button: '', betAmountLabel: '', tickerIdle: '', tickerSpin: '', bannerText: '' },
	maxWin: 8888,
});

// Les vrais modes de mise de Louvo ne sont jamais fournis par le serveur dans
// stateMeta.betModeMeta (reste generique du modele de base, jamais adapte) -
// on les injecte nous-memes ici pour que l'achat de bonus ne plante plus.
const LOUVO_REAL_BET_MODES = {
	BONUS_AFTER_DARK: LOUVO_BET_MODE_SHAPE('BONUS_AFTER_DARK', 150.0),
	BONUS_SPEED_DATING: LOUVO_BET_MODE_SHAPE('BONUS_SPEED_DATING', 80.0),
	MATCH_BOOST: LOUVO_BET_MODE_SHAPE('MATCH_BOOST', 3.0),
	MATCH_FRENZY: LOUVO_BET_MODE_SHAPE('MATCH_FRENZY', 60.0),
	LIKE_STORM: LOUVO_BET_MODE_SHAPE('LIKE_STORM', 60.0),
};
"""
n = content.count(old_a)
if n != 1:
    results.append(f"ERREUR (constantes) : {n} fois.")
else:
    content = content.replace(old_a, new_a, 1)
    results.append("OK (constantes ajoutees)")

old_b = "\tsetContextApp({ stateApp });\n};"
new_b = "\tsetContextApp({ stateApp });\n\tObject.assign(stateMeta.betModeMeta, LOUVO_REAL_BET_MODES);\n};"
n = content.count(old_b)
if n != 1:
    results.append(f"ERREUR (injection) : {n} fois.")
else:
    content = content.replace(old_b, new_b, 1)
    results.append("OK (injection dans setContext)")

with open(path, "w") as f:
    f.write(content)

for r in results:
    print(r)
