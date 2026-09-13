<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventWin =
		| { type: 'winShow' }
		| { type: 'winHide' }
		| { type: 'winUpdate'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { Container, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { OnMount } from 'components-shared';

	import WinCoins from './WinCoins.svelte';
	import WinLevelScreen from './WinLevelScreen.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import { SYMBOL_SIZE } from '../game/constants';
	import { getContext } from '../game/context';
	import { stateBet } from 'state-shared';

	const context = getContext();

	// VOTRE cadre a la place du fond noir du montant, sous BIG WIN.
	const CADRE_PETIT = true; // <<< false pour revenir au fond noir
	const CADRE_PETIT_LARGEUR = SYMBOL_SIZE * 2.6; // <<< LA taille du cadre
	const CADRE_PETIT_RATIO = 1536 / 1024; // proportions de l'image
	// Rattrapage vertical : recentre le DESSIN sur le montant.
	const CADRE_PETIT_DECALAGE = 0.0361; // <<< monter (negatif) ou descendre
	const cadrePetitHauteur = CADRE_PETIT_LARGEUR / CADRE_PETIT_RATIO;

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		winShow: () => (show = true),
		winHide: () => (show = false),
		spinStart: () => {
			if (show) oncomplete();
		},
		winUpdate: async (emitterEvent) => {
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});
</script>

<FadeContainer {show}>
	{#if winLevelData}
		{@const isBigWin = winLevelData.type === 'big'}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration} oncomplete={() => onCountUpComplete()}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />

				<OnMount
					onmount={async () => {
						if (isBigWin) {
							// A partir de BIG WIN : compte depuis zero, reste affiche
							// le temps prevu pour la mise en scene.
							await startCountUp();
							await waitForTimeout(300);
							if (!stateBet.stopOnWin) {
								await waitForTimeout(duration);
								oncomplete();
							}
						} else {
							// En dessous de BIG WIN : affichage instantane, pas de
							// comptage depuis zero, enchainement direct sur le tour
							// suivant, sans aucune attente.
							finishCountUp();
							if (!stateBet.stopOnWin) {
								oncomplete();
							}
						}
						// Si stopOnWin est actif, reste affiche jusqu'a un clic manuel
						// (PressToContinue) ou le prochain spin, quel que soit le palier.
					}}
				/>

				<MainContainer>
					<Container
						x={context.stateGameDerived.boardLayout().x}
						y={context.stateGameDerived.boardLayout().y}
					>
						{#if winLevelData?.animation}
							<!-- Image du palier, fond noir et montant : tout se regle
								dans WinLevelScreen.svelte. -->
							<WinLevelScreen
								alias={winLevelData.alias}
								montant={bookEventAmountToCurrencyString(countUpAmount)}
							/>
						{:else}
							{#if CADRE_PETIT}
								<Sprite
									anchor={0.5}
									key="totalWinFrame"
									y={CADRE_PETIT_DECALAGE * cadrePetitHauteur}
									width={CADRE_PETIT_LARGEUR}
									height={cadrePetitHauteur}
								/>
							{:else}
								<Rectangle
									anchor={0.5}
									width={SYMBOL_SIZE * 2.6}
									height={SYMBOL_SIZE * 0.8}
									backgroundColor={0x000000}
									alpha={0.78}
								/>
							{/if}
							<ResponsiveBitmapText
								anchor={0.5}
								maxWidth={context.stateLayoutDerived.canvasSizes().width /
									context.stateLayoutDerived.mainLayout().scale}
								text={bookEventAmountToCurrencyString(countUpAmount)}
								style={{
									fontFamily: 'gold', fill: 0xff2d6a,
									fontSize: SYMBOL_SIZE,
									align: 'center',
									fontWeight: 'bold',
									letterSpacing: 0,
								}}
							/>
						{/if}
					</Container>
				</MainContainer>

				{#if countUpCompleted}
					<!-- La somme a fini de monter : on coupe la boucle de pieces sans attendre le clic. -->
					<OnMount onmount={() => context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' })} />
				{/if}
				<WinCoins emit={!countUpCompleted} levelAlias={winLevelData?.alias} />

				<PressToContinue onpress={() => (countUpCompleted ? oncomplete() : finishCountUp())} />
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
