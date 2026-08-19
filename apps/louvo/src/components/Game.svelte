<script lang="ts">
	import { onMount } from 'svelte';

	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Text, REM, Container, Rectangle, Sprite } from 'pixi-svelte';
	import { stateModal } from 'state-shared';

	import { UiGameName } from 'components-ui-pixi';
	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import LouvoBottomBar from './LouvoBottomBar.svelte';
	import AfterDarkStreakDisplay from './AfterDarkStreakDisplay.svelte';
	import WinLinesDisplay from './WinLinesDisplay.svelte';
	import LouvoSettingsMenu from './LouvoSettingsMenu.svelte';
	import LouvoBonusMenu from './LouvoBonusMenu.svelte';
	import { GameVersion, Modals } from 'components-ui-html';

	import { getContext } from '../game/context';
	import EnableSound from './EnableSound.svelte';
	import EnableGameActor from './EnableGameActor.svelte';
	import ResumeBet from './ResumeBet.svelte';
	import Sound from './Sound.svelte';
	import Background from './Background.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
import LouvoIntroScreen from './LouvoIntroScreen.svelte';
	import BoardFrame from './BoardFrame.svelte';
	import Board from './Board.svelte';
	import Anticipations from './Anticipations.svelte';
	import Win from './Win.svelte';
	import SpecialRevealOverlay from './SpecialRevealOverlay.svelte';
import DevRevealPanel from './DevRevealPanel.svelte';
	import FreeSpinIntro from './FreeSpinIntro.svelte';
	import FreeSpinCounter from './FreeSpinCounter.svelte';
	import FreeSpinOutro from './FreeSpinOutro.svelte';
	import Transition from './Transition.svelte';

	const context = getContext();

	onMount(() => (context.stateLayout.showLoadingScreen = true));

	let bonusMenuOpen = $state(false);
	let showIntroScreen = $state(false);

	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
		bonusMenuShow: () => (bonusMenuOpen = true),
	});
</script>

<App>
	<EnableSound />
	<EnableHotkey />
	<EnableGameActor />
	<EnablePixiExtension />

	<Background />

	{#if context.stateLayout.showLoadingScreen}
		<LoadingScreen
			onloaded={() => {
				context.stateLayout.showLoadingScreen = false;
				showIntroScreen = true;
			}}
		/>
	{:else if showIntroScreen}
		<LouvoIntroScreen onpress={() => (showIntroScreen = false)} />
	{:else}
		<ResumeBet />
		<!--
			The reason why <Sound /> is rendered after clicking the loading screen:
			"Autoplay with sound is allowed if: The user has interacted with the domain (click, tap, etc.)."
			Ref: https://developer.chrome.com/blog/autoplay
		-->
		<Sound />

		<MainContainer>
			<Board />
			<Anticipations />
		</MainContainer>

		<MainContainer>
			<BoardFrame />
				<AfterDarkStreakDisplay
					tier2={{
						filled:
							context.stateGame.streakTier === 1
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier >= 2
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 2,
					}}
					tier3={{
						filled:
							context.stateGame.streakTier === 2
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier >= 3
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 3,
					}}
					tier4={{
						filled:
							context.stateGame.streakTier === 3
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier >= 4
									? 0
									: 6,
						achieved: context.stateGame.streakTier >= 4,
					}}
					tier5x={{
						filled:
							context.stateGame.streakTier === 4
								? 6 - context.stateGame.streakLikes
								: context.stateGame.streakTier > 4
									? 0
									: 6,
						achieved: context.stateGame.streakTier > 4,
					}}
				/>
		</MainContainer>

		<Container x={20}>
			<UiGameName name="LINES GAME" />
		</Container>
		<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
			<Sprite key="louvoLogo" anchor={{ x: 1, y: 0 }} width={100} height={72.8} />
		</Container>
		<MainContainer standard alignVertical="bottom">
			<Container
				x={context.stateLayoutDerived.mainLayoutStandard().width * 0.5}
				y={context.stateLayoutDerived.mainLayoutStandard().height - 10}
			>
				<LouvoBottomBar />
			</Container>
		</MainContainer>

		{#if stateUi.menuOpen}
			<Rectangle
				eventMode="static"
				cursor="pointer"
				alpha={0.5}
				anchor={0.5}
				backgroundColor={BLACK}
				width={context.stateLayoutDerived.canvasSizes().width}
				height={context.stateLayoutDerived.canvasSizes().height}
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
				onpointerup={() => (stateUi.menuOpen = false)}
			/>
			<Container
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
			>
				<LouvoSettingsMenu />
			</Container>
		{/if}

		{#if bonusMenuOpen}
			<Rectangle
				eventMode="static"
				cursor="pointer"
				alpha={0.5}
				anchor={0.5}
				backgroundColor={BLACK}
				width={context.stateLayoutDerived.canvasSizes().width}
				height={context.stateLayoutDerived.canvasSizes().height}
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
				onpointerup={() => (bonusMenuOpen = false)}
			/>
			<Container
				x={context.stateLayoutDerived.canvasSizes().width * 0.5}
				y={context.stateLayoutDerived.canvasSizes().height * 0.5}
			>
				<LouvoBonusMenu onclose={() => (bonusMenuOpen = false)} />
			</Container>
		{/if}
		<Win />
		<SpecialRevealOverlay />
		<MainContainer zIndex={100}>
			<WinLinesDisplay />
		</MainContainer>
		<DevRevealPanel />
		<FreeSpinIntro />
		{#if ['desktop', 'landscape'].includes(context.stateLayoutDerived.layoutType())}
			<FreeSpinCounter />
		{/if}
		<FreeSpinOutro />
		<Transition />

	{/if}
</App>

<Modals>
	{#snippet version()}
		<GameVersion version="0.0.0" />
	{/snippet}
	{#snippet gameRules()}
		{@html `<style>
	.louvo-rules {
		color: #ffffff;
		line-height: 1.5;
		max-height: 80vh;
		overflow-y: auto;
		padding-right: 12px;
		box-sizing: border-box;
	}
	.louvo-rules h2 { color: #ff2d6a; margin-top: 24px; }
	.louvo-rules h3 { color: #ff8fb3; margin-top: 16px; }
	.louvo-paytable-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
		gap: 12px;
		margin: 12px 0;
	}
	.louvo-paytable-item {
		text-align: center;
		font-size: 12px;
	}
	.louvo-paytable-item img {
		width: 56px;
		height: 56px;
		object-fit: contain;
		border-radius: 6px;
		display: block;
		margin: 0 auto 4px auto;
	}
	.louvo-paytable-item span {
		display: block;
	}
	.ln-wrap {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
		gap: 10px;
		margin: 12px 0;
	}
	.ln-item {
		text-align: center;
	}
	.ln-label {
		font-size: 11px;
		color: #ff8fb3;
		margin-bottom: 2px;
	}
	.ln-grid {
		display: grid;
		grid-template-columns: repeat(5, 8px);
		grid-template-rows: repeat(5, 8px);
		gap: 1px;
		background: #000000;
		padding: 2px;
		margin: 0 auto;
		width: fit-content;
	}
	.ln-cell {
		width: 8px;
		height: 8px;
		background: #2a1018;
	}
	.ln-cell.active {
		background: #ff2d6a;
	}
</style>
<div class="louvo-rules">
	<h2>ABOUT THE GAME</h2>
	<p>Welcome to Louvo! Swipe into a 5-reel, 5-row grid packed with 19 paylines, and see who really matches. The maximum win of 15,000x your bet can be hit in any game mode.</p>

	<h2>FEATURES</h2>

	<h3>THE MATCH DUEL</h3>
	<p>When MATCH symbols land in a winning combination, two multiplier values face off in a duel. Either one can win, it's a coin flip, and only the surviving multiplier is applied to the win.</p>

	<h3>SUPER LIKE</h3>
	<p>The SUPER LIKE symbol reveals a multiplier and sends out between 1 and 6 Wilds to random empty positions on the grid.</p>

	<h3>SPEED DATING &amp; AFTER DARK</h3>
	<p>Land 3 DATE scatters to unlock SPEED DATING: 10 free spins under a brighter sky. Land 4 DATE scatters to unlock AFTER DARK: 10 free spins once the sun goes down, with an escalating Match Streak that can guarantee bigger and bigger MATCH wins the longer it runs.</p>
	<p>During free spins, landing 2 extra scatters awards 2 more spins; landing 3 extra scatters awards 4 more spins.</p>

	<h2>PAYTABLE</h2>
	<p>Payouts shown are multiples of your total bet.</p>
	<div class="louvo-paytable-grid">
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/portraits/h1_le_r.png" alt="Le R" />
			<span>5&nbsp;&nbsp;20.00</span>
			<span>4&nbsp;&nbsp;10.00</span>
			<span>3&nbsp;&nbsp;4.00</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/portraits/h2_inso.png" alt="Inso" />
			<span>5&nbsp;&nbsp;16.00</span>
			<span>4&nbsp;&nbsp;8.00</span>
			<span>3&nbsp;&nbsp;2.00</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/portraits/h3_shanna.png" alt="Shanna" />
			<span>5&nbsp;&nbsp;12.00</span>
			<span>4&nbsp;&nbsp;6.00</span>
			<span>3&nbsp;&nbsp;1.50</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/portraits/h4_manu.png" alt="Manu" />
			<span>5&nbsp;&nbsp;8.00</span>
			<span>4&nbsp;&nbsp;4.00</span>
			<span>3&nbsp;&nbsp;1.00</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/portraits/h5_indigo.png" alt="Indigo" />
			<span>5&nbsp;&nbsp;6.00</span>
			<span>4&nbsp;&nbsp;3.00</span>
			<span>3&nbsp;&nbsp;0.70</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/portraits/h6_coca_cherry.png" alt="Coca Cherry" />
			<span>5&nbsp;&nbsp;4.00</span>
			<span>4&nbsp;&nbsp;2.00</span>
			<span>3&nbsp;&nbsp;0.50</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/basic-symbols/l1_verifie.png" alt="Verified" />
			<span>5&nbsp;&nbsp;2.00</span>
			<span>4&nbsp;&nbsp;1.00</span>
			<span>3&nbsp;&nbsp;0.20</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/basic-symbols/l2_message.png" alt="Message" />
			<span>5&nbsp;&nbsp;2.00</span>
			<span>4&nbsp;&nbsp;1.00</span>
			<span>3&nbsp;&nbsp;0.20</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/basic-symbols/l3_flamme.png" alt="Flame" />
			<span>5&nbsp;&nbsp;2.00</span>
			<span>4&nbsp;&nbsp;1.00</span>
			<span>3&nbsp;&nbsp;0.20</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/basic-symbols/l4_coeur.png" alt="Heart" />
			<span>5&nbsp;&nbsp;2.00</span>
			<span>4&nbsp;&nbsp;1.00</span>
			<span>3&nbsp;&nbsp;0.20</span>
		</div>
		<div class="louvo-paytable-item">
			<img src="/assets/sprites/special/wild.png" alt="Wild" />
			<span>5&nbsp;&nbsp;20.00</span>
		</div>
	</div>
	<p>The RTP for this game is 96.5%.</p>

	<h2>SPECIAL SYMBOLS</h2>
	<p><strong>WILD</strong> substitutes for all symbols on the paytable. Wilds only appear on the grid through the SUPER LIKE feature.</p>
	<p><strong>MATCH</strong> triggers a duel between two multiplier values, deciding the multiplier applied to the win.</p>
	<p><strong>SUPER LIKE</strong> reveals a multiplier and sends out extra Wilds to the grid.</p>
	<p>Possible multiplier values for MATCH and SUPER LIKE are: 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x, 15x, 20x, 25x, 50x, 75x, 100x, 200x.</p>
	<p><strong>DATE</strong> is the scatter symbol. Land 3 or 4 to unlock SPEED DATING or AFTER DARK.</p>

	<h2>WAYS TO WIN</h2>
	<p>You win when matching symbols land on adjacent reels, starting from the leftmost reel, along one of 19 fixed paylines. Only the highest win per line is paid.</p>
	<div class="ln-wrap"><div class="ln-item"><div class="ln-label">1</div><div class="ln-grid"><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">2</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">3</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">4</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">5</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div><div class="ln-cell active"></div></div></div><div class="ln-item"><div class="ln-label">6</div><div class="ln-grid"><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">7</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">8</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">9</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">10</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">11</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">12</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">13</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div></div></div><div class="ln-item"><div class="ln-label">14</div><div class="ln-grid"><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div></div></div><div class="ln-item"><div class="ln-label">15</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">16</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">17</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">18</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div><div class="ln-item"><div class="ln-label">19</div><div class="ln-grid"><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell active"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div><div class="ln-cell"></div></div></div></div>

	<h2>BUY BONUS</h2>
	<p>Louvo lets you jump straight into the action from the BONUS button.</p>
	<p><strong>DATE X5</strong> — 3x your bet — increases the chance of triggering a bonus round.</p>
	<p><strong>MATCH 2+</strong> — 60x your bet — guarantees MATCH symbols on the next spin.</p>
	<p><strong>SUPER LIKE</strong> — 60x your bet — guarantees a Super Like on the next spin.</p>
	<p><strong>SPEED DATING</strong> — 80x your bet — instantly unlocks 10 free spins in the daytime setting.</p>
	<p><strong>AFTER DARK</strong> — 150x your bet — instantly unlocks 10 free spins in the nighttime setting.</p>

	<h2>BET</h2>
	<p>Bet levels range from 0.10 to 2000 in your selected currency. Bonus buys and other special feature purchases can cost more than the maximum base bet.</p>
</div>`}
	{/snippet}
</Modals>
