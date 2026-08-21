<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';
	import { getSymbolX } from '../game/utils';
	import { getContext } from '../game/context';
	import { stateBet } from 'state-shared';
	import { BOARD_SIZES, SYMBOL_HEIGHT, REEL_PADDING } from '../game/constants';

	type Position = { reelIndex: number; rowIndex: number };

	type Props = {
		reelIndex: number;
		positions?: Position[];
	};
	const props: Props = $props();
	const context = getContext();

	const HEART_SIZE = 28; // meme taille que les coeurs du presentoir
	const BASE_DELAY = 900; // laisse le temps aux rouleaux de finir de se poser (vitesse normale)
	const effectiveDelay = () => BASE_DELAY / (stateBet.isSuperTurbo ? 4 : stateBet.isTurbo ? 2 : 1);
	// Attente robuste : au lieu de deviner un minuteur, on verifie l'etat
	// REEL de chaque rouleau (comme pour l'anticipation) - garantit que les
	// coeurs ne partent JAMAIS pendant qu'un rouleau tourne encore.
	const waitForAllReelsStopped = async () => {
		// Phase 1 : attend que les rouleaux du TOUR COURANT demarrent (en free
		// spins, le composant est monte AVANT le depart des rouleaux, encore
		// "stopped" du tour precedent) - securite 4s si le tour ne demarre pas.
		const startWait = performance.now();
		while (
			context.stateGame.board.every((reel) => reel.reelState.motion === 'stopped') &&
			performance.now() - startWait < 4000
		) {
			await new Promise((r) => setTimeout(r, 50));
		}
		// Phase 2 : attend l'arret complet.
		while (context.stateGame.board.some((reel) => reel.reelState.motion !== 'stopped')) {
			await new Promise((r) => setTimeout(r, 50));
		}
	};

	const originX = getSymbolX(props.reelIndex);
	const originY = BOARD_SIZES.height / 2 + 162.7;

	const getRowY = (rowIndex: number) => SYMBOL_HEIGHT * (rowIndex + REEL_PADDING);

	// Securite : exclut toute position ciblee sur la colonne de la banniere
	// Super Like elle-meme OU sur la colonne d'une AUTRE banniere active en
	// meme temps (ex: Match Duel sur un autre rouleau du meme spin) - un
	// coeur ne doit JAMAIS atterrir sur une case occupee par une banniere.
	const positions = (props.positions ?? []).filter(
		(p) => p.reelIndex !== props.reelIndex,
	);
	const targets = positions.map((p) => ({
		x: getSymbolX(p.reelIndex),
		y: getRowY(p.rowIndex),
	}));

	type Heart = { id: number; x: number; y: number; alpha: number; scale: number };

	let hearts = $state<Heart[]>(
		targets.map((_, i) => ({ id: i, x: originX, y: originY, alpha: 0, scale: 0.5 })),
	);

	const easeOutQuad = (t: number) => 1 - (1 - t) * (1 - t);

	const fadeOut = (index: number) =>
		new Promise<void>((resolve) => {
			const duration = 180;
			const start = performance.now();

			const step = (now: number) => {
				const t = Math.min((now - start) / duration, 1);
				hearts[index].alpha = 1 - t;

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					resolve();
				}
			};

			requestAnimationFrame(step);
		});

	// Vole vers la cible et resout des que le coeur touche sa case - le
	// fondu de disparition part APRES en arriere-plan (fire-and-forget),
	// sans retarder le lancer du coeur suivant.
	const flyTo = (index: number) =>
		new Promise<void>((resolve) => {
			const target = targets[index];
			const duration = 550;
			const arcHeight = 60 + Math.random() * 30;
			const start = performance.now();

			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up', forcePlay: true });
			// Synchronisation presentoir : le barillet retire son coeur au moment exact du lancer.
			context.stateGame.superlikeHeartsLaunched = index + 1;
			// After Dark : le presentoir de palier descend d'un coeur par lancer.
			if (context.stateGame.tier === 'after_dark') {
				if (context.stateGame.streakTier === 0) context.stateGame.streakTier = 1;
				context.stateGame.streakLikes += 1;
				if (context.stateGame.streakLikes >= 6) {
					// Palier vide : affiche les cartes (DUEL du palier + '+3 free spins').
					context.stateGame.tierPassToShow = context.stateGame.streakTier;
					context.stateGame.streakTier += 1;
					context.stateGame.streakLikes = 0;
				}
			}

			const step = (now: number) => {
				const elapsed = now - start;
				const t = Math.min(elapsed / duration, 1);
				const eased = easeOutQuad(t);

				hearts[index].x = originX + (target.x - originX) * eased;
				hearts[index].y =
					originY + (target.y - originY) * eased - Math.sin(t * Math.PI) * arcHeight;
				hearts[index].alpha = t < 0.15 ? t / 0.15 : 1;
				hearts[index].scale = 0.5 + Math.min(t / 0.2, 1) * 0.5;

				if (t < 1) {
					requestAnimationFrame(step);
				} else {
					// Le symbole devient WILD exactement au moment ou le coeur
					// touche sa case (pas avant, pas apres).
					const pos = positions[index];
					if (pos) {
						const reelSymbol =
							context.stateGame.board[pos.reelIndex]?.reelState?.symbols[pos.rowIndex + 1];
						if (reelSymbol) {
							reelSymbol.rawSymbol = { name: 'W', wild: true };
						}
					}
					context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode', forcePlay: true });
					// Le coeur disparait immediatement : le vrai symbole WILD
					// prend le relais visuellement a cet instant precis.
					hearts[index].alpha = 0;
					resolve();
				}
			};

			requestAnimationFrame(step);
		});

	// Le book (reveal) contient deja les W sur les cases ciblees : des que le
	// rouleau d'une case s'arrete, on re-affiche un symbole normal (L4) - la
	// vraie transformation en WILD se fait uniquement a l'impact du coeur.
	const maskLandedWilds = () => {
		for (const pos of positions) {
			const reel = context.stateGame.board[pos.reelIndex];
			const reelSymbol = reel.reelState.symbols[pos.rowIndex + 1];
			if (reelSymbol?.rawSymbol?.name === 'W') {
				reelSymbol.rawSymbol = { name: 'L4' };
			}
		}
	};

	onMount(() => {
		// File du tour : gate = fin de la distribution precedente du MEME tour
		// (resolue d'office s'il n'y en a pas), doneResolve = signal de fin de
		// la notre (la chaine complete est attendue par winInfo/setTotalWin).
		const startGate = context.stateGame.superlikeStartGates.shift() ?? Promise.resolve();
		const doneResolve = context.stateGame.superlikeDoneResolvers.shift() ?? (() => {});
		context.stateGame.superlikeActiveThrows += 1;
		const wildWatcher = setInterval(maskLandedWilds, 16);
		(async () => {
			await waitForAllReelsStopped();
			clearInterval(wildWatcher);
			maskLandedWilds();
			// Chacun son tour : la distribution precedente doit avoir fini.
			await startGate;
			await new Promise((r) => setTimeout(r, effectiveDelay()));
			console.log('[SuperLike DEBUG] coeurs affiches:', hearts.length, '- positions cibles:', JSON.stringify(positions));
			for (let i = 0; i < hearts.length; i++) {
				try {
					await flyTo(i);
				} catch (error) {
					console.error('[SuperLike DEBUG] lancer du coeur', i, 'echoue :', error);
				}
			}
			context.stateGame.superlikeActiveThrows -= 1;
			// Cale l'affichage sur la verite du Math SDK (debordements compris) -
			// seulement a la fin de la DERNIERE distribution du tour (les cibles
			// math decrivent l'etat FINAL du tour, pas l'etat entre deux bannieres).
			if (context.stateGame.superlikeActiveThrows <= 0 && context.stateGame.tier === 'after_dark') {
				// Le math compte les paliers TERMINES ; l'affichage vit sur le palier EN COURS (+1).
				context.stateGame.streakTier = context.stateGame.streakTargetTier + 1;
				context.stateGame.streakLikes = context.stateGame.streakTargetHearts;
			}
			doneResolve();
		})();
	});
</script>

{#each hearts as heart (heart.id)}
	<Container x={heart.x} y={heart.y} alpha={heart.alpha} scale={heart.scale} zIndex={40}>
		<Sprite key="heartBullet" anchor={0.5} width={HEART_SIZE} height={HEART_SIZE} />
	</Container>
{/each}
