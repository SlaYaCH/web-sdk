import _ from 'lodash';
import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet, stateBetDerived, stateUi } from 'state-shared';
import { sequence } from 'utils-shared/sequence';
import { eventEmitter } from './eventEmitter';
import { playBookEvent } from './utils';
import { winLevelMap, type WinLevel, type WinLevelData } from './winLevelMap';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position } from './types';
import config from './config';
const freeSpinMusicName = () => (stateGame.tier === 'after_dark' ? 'bgm_after_dark' : 'bgm_speed_dating');

const winLevelSoundsPlay = ({ winLevelData }: { winLevelData: WinLevelData }) => {
	if (winLevelData?.alias === 'max') eventEmitter.broadcastAsync({ type: 'uiHide' });
	if (winLevelData?.sound?.sfx) {
		eventEmitter.broadcast({ type: 'soundOnce', name: winLevelData.sound.sfx });
	}
	if (winLevelData?.sound?.bgm) {
		eventEmitter.broadcast({ type: 'soundMusic', name: winLevelData.sound.bgm });
	}
	if (winLevelData?.type === 'big') {
		eventEmitter.broadcast({ type: 'soundLoop', name: 'sfx_bigwin_coinloop' });
	}
};
const winLevelSoundsStop = () => {
	eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' });
	if (stateBet.activeBetModeKey === 'SUPERSPIN' || stateGame.gameType === 'freegame') {
		eventEmitter.broadcast({ type: 'soundMusic', name: freeSpinMusicName() });
	} else {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main_louvo' });
	}
	eventEmitter.broadcastAsync({ type: 'uiShow' });
};
// Retour en base game : on repose une grille de base ALEATOIRE (aucun W, M, K
// ou S) pour ne jamais rester sur la derniere grille After Dark.
const BASE_RANDOM_SYMBOLS = ['L1', 'L2', 'L3', 'L4', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6'] as const;
const resetBoardToRandomBase = () => {
	for (const reel of stateGame.board) {
		for (const reelSymbol of reel.reelState.symbols) {
			const name = BASE_RANDOM_SYMBOLS[Math.floor(Math.random() * BASE_RANDOM_SYMBOLS.length)];
			reelSymbol.rawSymbol = { name };
		}
	}
};
// Cartes de palier After Dark en attente : les affiche 2 s, SEULES, avant la
// suite du tour special. Appelee au premier evenement du tour concerne :
// updateFreeSpin quand il existe, sinon la premiere banniere (les books
// montrent des tours speciaux SANS updateFreeSpin). tierPassPending est vide
// au premier passage : les appels suivants ne font rien.
const tierPassCardsShow = async () => {
	if (!stateGame.tierPassPending) return;
	stateGame.tierPassToShow = stateGame.tierPassPending;
	stateGame.tierPassPending = 0;
	// AfterDarkTierPass s'auto-masque au bout de 1800 ms.
	await new Promise((resolve) => setTimeout(resolve, 2000));
};
const animateSymbols = async ({ positions }: { positions: Position[] }) => {
	eventEmitter.broadcast({ type: 'boardShow' });
	await eventEmitter.broadcastAsync({
		type: 'boardWithAnimateSymbols',
		symbolPositions: positions,
	});
};
export const bookEventHandlerMap: BookEventHandlerMap<BookEvent, BookEventContext> = {
	reveal: async (bookEvent: BookEventOfType<'reveal'>, { bookEvents }: BookEventContext) => {
		// Attend la fin des lancers de coeurs d'un tour PRECEDENT avant d'enchainer
		// (garde anti-blocage : jamais la promesse creee pour le tour courant).
		if (stateGame.superlikeAnimationPromise && stateGame.superlikeAnimationEpoch < stateGame.bannerEpoch) {
			await stateGame.superlikeAnimationPromise;
			stateGame.superlikeAnimationPromise = null;
		}
		// Chaque nouveau tour (free spins compris) cloture les bannieres du tour precedent.
		// Fermeture differee : les bannieres du tour precedent se ferment une fois
		// les rouleaux partis (comme lorsqu'un gain retarde le tour suivant) - la
		// colonne de W du book n'est jamais visible a l'arret, meme en turbo.
		setTimeout(() => {
			stateGame.bannerEpoch += 1;
		}, 150);
		// Purge les drapeaux d'anticipation restes bloques d'un tour precedent
		// (l'animation ne se termine pas toujours, le drapeau restait a true).
		for (const reel of stateGame.board) {
			if (reel.reelState?.anticipating) reel.reelState.anticipating = false;
		}
		// L'anticipation calculee par le math compte AUSSI les scatters des rangees
		// de padding (invisibles) : on la neutralise tant que moins de 2 DATE
		// VISIBLES ne sont tombes sur les rouleaux precedents.
		{
			let cumulVisibles = 0;
			bookEvent.anticipation = bookEvent.anticipation.map((value, i) => {
				const keep = cumulVisibles >= 2 ? value : 0;
				cumulVisibles += bookEvent.board[i].slice(1, -1).filter((s) => s.name === 'S').length;
				return keep;
			});
		}
		const isBonusGame = checkIsMultipleRevealEvents({ bookEvents });
		if (isBonusGame) {
			eventEmitter.broadcast({ type: 'stopButtonEnable' });
			recordBookEvent({ bookEvent });
		}
		// Turbo et super turbo DESACTIVES pendant les bonus : aucun interet en
		// free spins (le joueur ne clique pas) et source de bugs visuels. Un
		// reglage reactive via le menu en cours de bonus est coupe ici, a
		// CHAQUE tour (l'entree de bonus le coupait deja dans freeSpinTrigger).
		if (bookEvent.gameType === 'freegame') {
			stateBetDerived.updateIsTurbo(false, { persistent: true });
			stateBet.isSuperTurbo = false;
		}
		stateGame.gameType = bookEvent.gameType;
		await stateGameDerived.enhancedBoard.spin({
			revealEvent: bookEvent,
			paddingBoard: config.paddingReels[bookEvent.gameType],
		});
		eventEmitter.broadcast({ type: 'soundScatterCounterClear' });
	},
	// Louvo : événements dédiés émis directement par le math-sdk au moment
	// du duel (avant que M/K ne soient remplacés par W) - plus besoin de
	// deviner depuis le plateau, ni de risquer qu'un simple WILD déclenche
	// une bannière par erreur.
	matchDuelReveal: async (bookEvent: BookEventOfType<'matchDuelReveal'>) => {
		// Tour special SANS updateFreeSpin (cas observe dans les books) :
		// les cartes du palier s'affichent AVANT la premiere banniere MATCH.
		await tierPassCardsShow();
		// Ne bloque plus la suite de la sequence : la banniere reste affichee
		// indefiniment (voir SpecialRevealOverlay) et se fermera uniquement au
		// prochain spin (spinStart -> forceClose), pas sur un minuteur.
		eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'M',
			multiplier: bookEvent.multiplier,
			duelValues: bookEvent.duelValues,
		});
	},
	superlikeReveal: async (bookEvent: BookEventOfType<'superlikeReveal'>) => {
		// Si un palier attend encore ses cartes, elles passent avant la banniere.
		await tierPassCardsShow();
		// Un Super Like d'un TOUR PRECEDENT encore en cours (tour sans gain :
		// rien d'autre ne l'attendait) : on le laisse finir avant d'empiler le notre.
		if (stateGame.superlikeAnimationPromise && stateGame.superlikeAnimationEpoch < stateGame.bannerEpoch) {
			await Promise.race([
				stateGame.superlikeAnimationPromise,
				new Promise((resolve) => setTimeout(resolve, 12000)),
			]);
			stateGame.superlikeAnimationPromise = null;
		}
		// Deux SUPER LIKE dans le MEME tour : leurs bookEvents arrivent AVANT le
		// reveal, donc ce handler ne doit JAMAIS bloquer la sequence (sinon les
		// rouleaux ne partent pas - c'etait le blocage de ~10 s). A la place,
		// chaque distribution recoit une gate (= fin de la precedente) que le
		// composant attendra, et la promesse globale devient la CHAINE complete.
		const previousTail =
			stateGame.superlikeAnimationEpoch === stateGame.bannerEpoch
				? stateGame.superlikeAnimationPromise
				: null;
		// Compteur de coeurs CUMULE sur le tour (chaque barillet se cale dessus
		// via son offset) : remis a zero seulement au PREMIER Super Like du tour.
		if (!previousTail) stateGame.superlikeHeartsLaunched = 0;
		let throwDone!: () => void;
		const throwPromise = new Promise<void>((resolve) => (throwDone = resolve));
		stateGame.superlikeStartGates.push(previousTail ?? Promise.resolve());
		stateGame.superlikeDoneResolvers.push(throwDone);
		stateGame.superlikeAnimationEpoch = stateGame.bannerEpoch;
		stateGame.superlikeAnimationPromise = previousTail
			? previousTail.then(() => throwPromise)
			: throwPromise;
		// Ne bloque plus la suite de la sequence, meme raison que matchDuelReveal.
		eventEmitter.broadcast({
			type: 'specialRevealShow',
			reelIndex: bookEvent.reelIndex,
			symbol: 'K',
			multiplier: bookEvent.multiplier,
			likePositions: bookEvent.likePositions,
		});
		// Cible du Match Streak : la descente visuelle se fait coeur par coeur
		// dans SuperlikeHeartThrow, puis se cale sur ces valeurs du Math SDK.
		stateGame.streakTargetTier = bookEvent.streakTier;
		stateGame.streakTargetHearts = bookEvent.streakHearts;
	},
	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		// Attend la fin des lancers de coeurs Super Like avant d'afficher les lignes de gains.
		if (stateGame.superlikeAnimationPromise) {
			await Promise.race([
				stateGame.superlikeAnimationPromise,
				new Promise((resolve) => setTimeout(resolve, 12000)),
			]);
			stateGame.superlikeAnimationPromise = null;
		}
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		// Instant de depart de la presentation des lignes : sert plus bas a ne
		// completer que le temps qui manque VRAIMENT a la fin.
		const winLinesStartedAt = performance.now();
		if (bookEvent.wins.length > 0) {
			// Affichee tout de suite (pas apres la surbrillance des symboles),
			// directement quand le 5eme rouleau vient de s'arreter.
			eventEmitter.broadcast({ type: 'winLinesShow', wins: bookEvent.wins });
		}
		await sequence(bookEvent.wins, async (win) => {
			await animateSymbols({ positions: win.positions });
		});
		if (bookEvent.wins.length > 0) {
			// Duree d'UNE ligne (voir WinLineReveal.svelte) : 120 (apparition)
			// + 700 (maintien) + 150 (ligne disparait) + 300 (attente) + 250 (montant
			// disparait). Les lignes s'enchainent avec WIN_LINE_STAGGER d'ecart : la
			// presentation complete dure donc plus longtemps des qu'il y en a
			// plusieurs. L'attente etait FIXE (une seule ligne) : en turbo/super turbo,
			// ou la surbrillance des symboles est quasi instantanee et n'absorbe plus
			// le retard, le tour suivant partait par-dessus l'animation inachevee.
			// Valeurs verifiees dans le code : WinLineReveal = 120 + 700 + 150 + 300
			// + 250 par ligne, WinLinesDisplay = 200 ms entre deux lignes. La derniere
			// ligne se termine donc WIN_LINE_STAGGER x (nb lignes - 1) apres la
			// premiere. Les lignes ayant demarre AVANT la surbrillance des symboles,
			// celle-ci absorbe deja une partie de ce decalage : on garde la pause
			// d'origine et on ne rajoute QUE le manque. Vitesse normale : attente
			// inchangee. Turbo/super turbo (surbrillance quasi instantanee) : allongee
			// juste assez pour que la derniere ligne finisse avant le tour suivant.
			const WIN_LINE_DURATION = 120 + 700 + 150 + 300 + 250;
			const WIN_LINE_STAGGER = 200;
			const winLinesElapsed = performance.now() - winLinesStartedAt;
			const staggerLeft = Math.max(
				0,
				WIN_LINE_STAGGER * (bookEvent.wins.length - 1) - winLinesElapsed,
			);
			await new Promise((r) => setTimeout(r, WIN_LINE_DURATION + staggerLeft));
		}
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
		// Fin de CHAQUE tour, en base game COMME en free spins (finalWin n'existe
		// qu'en toute fin de book) : le tour n'est pas fini tant que des coeurs
		// Super Like volent. Un tour SANS gain n'a pas de winInfo et rien d'autre
		// ne les attendrait - le spin suivant fermait la banniere en pleine
		// animation et la colonne de W du book apparaissait (bug turbo).
		if (stateGame.superlikeAnimationPromise) {
			await Promise.race([
				stateGame.superlikeAnimationPromise,
				new Promise((resolve) => setTimeout(resolve, 12000)),
			]);
			stateGame.superlikeAnimationPromise = null;
		}
	},
	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		stateBetDerived.updateIsTurbo(false, { persistent: true });
		stateBet.isSuperTurbo = false;
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_superfreespin' });
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		await eventEmitter.broadcastAsync({ type: 'transition' });
		// L'ecran d'annonce s'affiche D'ABORD ; le changement de decor (grille
		// After Dark, fond nuit) se fait ensuite SOUS l'annonce, une fois son
		// fondu d'entree termine - plus aucun apercu de l'ancienne slot.
		// L'annonce recoit son tier directement : la bonne image des la premiere
		// frame (stateGame.tier n'est pose que 450 ms plus tard, sous l'annonce).
		eventEmitter.broadcast({ type: 'freeSpinIntroShow', tier: bookEvent.tier ?? 'speed_dating' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'jng_intro_fs' });
		await new Promise((r) => setTimeout(r, 450));
		stateGame.tier = bookEvent.tier ?? 'speed_dating';
		eventEmitter.broadcast({ type: 'soundMusic', name: freeSpinMusicName() });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinIntroUpdate',
			totalFreeSpins: bookEvent.totalFs,
		});
		stateGame.gameType = 'freegame';
		stateGame.streakTier = 0;
		stateGame.streakLikes = 0;
		eventEmitter.broadcast({ type: 'freeSpinIntroHide' });
		eventEmitter.broadcast({ type: 'boardFrameGlowShow' });
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		stateUi.freeSpinCounterShow = true;
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: undefined,
			total: bookEvent.totalFs,
		});
		stateUi.freeSpinCounterTotal = bookEvent.totalFs;
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerButtonShow' });
		eventEmitter.broadcast({ type: 'drawerFold' });
	},
	updateFreeSpin: async (bookEvent: BookEventOfType<'updateFreeSpin'>) => {
		// Palier After Dark franchi au tour precedent : cartes d'abord.
		await tierPassCardsShow();
		// Retrigger : le total augmente en cours de bonus -> message '+N FREE SPINS'.
		if (stateUi.freeSpinCounterTotal && bookEvent.total > stateUi.freeSpinCounterTotal) {
			stateGame.retriggerToShow = bookEvent.total - stateUi.freeSpinCounterTotal;
		}
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		stateUi.freeSpinCounterShow = true;
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: bookEvent.amount + 1,
			total: bookEvent.total,
		});
		stateUi.freeSpinCounterCurrent = bookEvent.amount + 1;
		stateUi.freeSpinCounterTotal = bookEvent.total;
	},
	freeSpinEnd: async (bookEvent: BookEventOfType<'freeSpinEnd'>) => {
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		eventEmitter.broadcast({ type: 'freeSpinOutroShow' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_youwon_panel' });
		winLevelSoundsPlay({ winLevelData });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinOutroCountUp',
			amount: bookEvent.amount,
			winLevelData,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'freeSpinOutroHide' });
		eventEmitter.broadcast({ type: 'freeSpinCounterHide' });
		stateUi.freeSpinCounterShow = false;
		await eventEmitter.broadcastAsync({ type: 'transition' });
		// TAP TO CONTINUE fait + transition qui couvre l'ecran : c'est SEULEMENT ici
		// qu'on quitte le decor After Dark et qu'on ferme les dernieres affiches
		// (sinon on apercoit la grille de base pendant le decompte du gain).
		stateGame.bannerEpoch += 2;
		stateGame.gameType = 'basegame';
		stateGame.tier = 'basegame';
		// Le plateau garderait sinon la derniere grille After Dark (colonne de W) :
		// on repose une grille de base aleatoire pendant que la transition couvre.
		resetBoardToRandomBase();
		stateGame.tierPassPending = 0;
		eventEmitter.broadcast({ type: 'boardFrameGlowHide' });
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerUnfold' });
		eventEmitter.broadcast({ type: 'drawerButtonHide' });
	},
	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];
		eventEmitter.broadcast({ type: 'winShow' });
		winLevelSoundsPlay({ winLevelData });
		await eventEmitter.broadcastAsync({
			type: 'winUpdate',
			amount: bookEvent.amount,
			winLevelData,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'winHide' });
	},
	finalWin: async (bookEvent: BookEventOfType<'finalWin'>) => {
		// Do nothing
	},
	createBonusSnapshot: async (bookEvent: BookEventOfType<'createBonusSnapshot'>) => {
		const { bookEvents } = bookEvent;
		function findLastBookEvent<T>(type: T) {
			return _.findLast(bookEvents, (bookEvent) => bookEvent.type === type) as
				| BookEventOfType<T>
				| undefined;
		}
		const lastFreeSpinTriggerEvent = findLastBookEvent('freeSpinTrigger' as const);
		const lastUpdateFreeSpinEvent = findLastBookEvent('updateFreeSpin' as const);
		const lastSetTotalWinEvent = findLastBookEvent('setTotalWin' as const);
		const lastUpdateGlobalMultEvent = findLastBookEvent('updateGlobalMult' as const);
		if (lastFreeSpinTriggerEvent) await playBookEvent(lastFreeSpinTriggerEvent, { bookEvents });
		if (lastUpdateFreeSpinEvent) playBookEvent(lastUpdateFreeSpinEvent, { bookEvents });
		if (lastSetTotalWinEvent) playBookEvent(lastSetTotalWinEvent, { bookEvents });
		if (lastUpdateGlobalMultEvent) playBookEvent(lastUpdateGlobalMultEvent, { bookEvents });
	},
};
