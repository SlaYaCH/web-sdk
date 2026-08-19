path = "apps/louvo/src/game/context.ts"
with open(path, "r") as f:
    content = f.read()

old = """import { i18nDerived } from '../i18n/i18nDerived';
export const setContext = () => {
	setContextEventEmitter<EmitterEvent>({ eventEmitter });
	setContextXstate({ stateXstate, stateXstateDerived });
	setContextLayout({ stateLayout, stateLayoutDerived });
	setContextApp({ stateApp });
};"""

new = """import { i18nDerived } from '../i18n/i18nDerived';
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

export const setContext = () => {
	setContextEventEmitter<EmitterEvent>({ eventEmitter });
	setContextXstate({ stateXstate, stateXstateDerived });
	setContextLayout({ stateLayout, stateLayoutDerived });
	setContextApp({ stateApp });
	Object.assign(stateMeta.betModeMeta, LOUVO_REAL_BET_MODES);
};"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les 5 vrais modes Louvo sont maintenant injectes au demarrage, betModeMeta ne sera plus jamais vide pour eux.")
