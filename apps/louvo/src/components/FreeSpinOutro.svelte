<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventFreeSpinOutro =
		| { type: 'freeSpinOutroShow' }
		| { type: 'freeSpinOutroHide' }
		| { type: 'freeSpinOutroCountUp'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { Container, Sprite } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { waitForResolve } from 'utils-shared/wait';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { OnMount } from 'components-shared';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import PressToContinue from './PressToContinue.svelte';
	import WinCoins from './WinCoins.svelte';

	// ============================================================
	// Le gain total de fin de bonus.
	//
	// Le panneau en bois venait de FreeSpinAnimation, pas du spine que
	// j'ai retire au lot 97 : votre cadre se posait donc DEDANS, d'ou sa
	// petite taille. Cet ecran ne passe plus par FreeSpinAnimation du
	// tout - votre cadre est dessine directement, avec la meme mecanique
	// que l'ecran de BIG WIN, qui lui se place correctement.
	//
	// Les proportions du cadre (3:2) sont celles de votre image et ne
	// doivent pas etre deformees : ne changez que CADRE_LARGEUR, la
	// hauteur suit toute seule.
	// ============================================================
	const CADRE_LARGEUR = SYMBOL_SIZE * 4.6; // <<< LA taille du cadre
	const CADRE_RATIO = 1024 / 1536; // proportions de l'image, a ne pas toucher
	const CADRE_Y = 0; // hauteur du cadre sur l'ecran
	const TEXTE_Y = 0; // hauteur du montant dans le cadre
	const TEXTE_TAILLE = SYMBOL_SIZE * 0.62; // taille des chiffres
	const TEXTE_LARGEUR = SYMBOL_SIZE * 2.9; // au-dela, le texte retrecit

	const context = getContext();

	let show = $state(true);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		freeSpinOutroShow: () => (show = true),
		freeSpinOutroHide: async () => (show = false),
		freeSpinOutroCountUp: async (emitterEvent) => {
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});
</script>

<FadeContainer {show}>
	{#if winLevelData}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration} oncomplete={() => onCountUpComplete()}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				<OnMount onmount={() => startCountUp()} />

				<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />

				<MainContainer>
					<Container
						x={context.stateGameDerived.boardLayout().x}
						y={context.stateGameDerived.boardLayout().y}
					>
						<Sprite
							anchor={0.5}
							key="totalWinFrame"
							y={CADRE_Y}
							width={CADRE_LARGEUR}
							height={CADRE_LARGEUR * CADRE_RATIO}
						/>
						<ResponsiveBitmapText
							anchor={0.5}
							y={CADRE_Y + TEXTE_Y}
							maxWidth={TEXTE_LARGEUR}
							text={bookEventAmountToCurrencyString(countUpAmount)}
							style={{
								fontFamily: 'gold',
								fontSize: TEXTE_TAILLE,
								align: 'center',
							}}
						/>
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
