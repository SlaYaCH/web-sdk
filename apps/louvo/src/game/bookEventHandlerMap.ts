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
		// Attend la fin des lancers d'un Super Like PRECEDENT avant d'en demarrer
		// un autre - sinon sa promesse serait ecrasee ici et le garde du reveal
		// ne pourrait plus l'attendre : deux distributions se chevaucheraient.
		if (stateGame.superlikeAnimationPromise && stateGame.superlikeAnimationEpoch < stateGame.bannerEpoch) {
			await stateGame.superlikeAnimationPromise;
			stateGame.superlikeAnimationPromise = null;
		}
		stateGame.superlikeHeartsLaunched = 0;
		console.log('[SuperLike DEBUG] bookEvent brut:', JSON.stringify(bookEvent));
		stateGame.superlikeAnimationEpoch = stateGame.bannerEpoch;
		stateGame.superlikeAnimationPromise = new Promise((resolve) => {
			stateGame.superlikeAnimationsDone = resolve;
		});
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
			await stateGame.superlikeAnimationPromise;
			stateGame.superlikeAnimationPromise = null;
		}
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		if (bookEvent.wins.length > 0) {
			// Affichee tout de suite (pas apres la surbrillance des symboles),
			// directement quand le 5eme rouleau vient de s'arreter.
			eventEmitter.broadcast({ type: 'winLinesShow', wins: bookEvent.wins });
		}
		await sequence(bookEvent.wins, async (win) => {
			await animateSymbols({ positions: win.positions });
		});
		if (bookEvent.wins.length > 0) {
			// Duree totale de l'animation d'une ligne (voir WinLineReveal.svelte) :
			// 120 (apparition) + 700 (maintien) + 150 (ligne disparait) + 300 (attente) + 250 (montant disparait)
			await new Promise((r) => setTimeout(r, 120 + 700 + 150 + 300 + 250));
		}
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
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
		eventEmitter.broadcast({ type: 'freeSpinIntroShow' });
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
		// Ferme toutes les bannieres restantes (Super Like/MATCH) en sortant du bonus.
		stateGame.bannerEpoch += 2;
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		stateGame.gameType = 'basegame';
		stateGame.tier = 'basegame';
		eventEmitter.broadcast({ type: 'boardFrameGlowHide' });
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
