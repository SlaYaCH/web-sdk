export default {
	fsIntroNumber: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/fsIntro/fs_screen.webp', import.meta.url).href,
			atlas: new URL('../../assets/spines/fsIntro/fs_screen.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/fsIntro/fs_screen_number.json', import.meta.url).href,
		},
	},
	fsOutroNumber: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/fsIntro/fs_screen.webp', import.meta.url).href,
			atlas: new URL('../../assets/spines/fsIntro/fs_screen.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/fsIntro/fs_total_number.json', import.meta.url).href,
		},
	},
	fsIntro: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/fsIntro/fs_screen.webp', import.meta.url).href,
			atlas: new URL('../../assets/spines/fsIntro/fs_screen.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/fsIntro/fs_screen.json', import.meta.url).href,
		},
	},
	H1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h1_le_r.webp', import.meta.url).href,
	},
	H2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h2_inso.webp', import.meta.url).href,
	},
	H3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h3_shanna.webp', import.meta.url).href,
	},
	H4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h4_manu.webp', import.meta.url).href,
	},
	H5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h5_indigo.webp', import.meta.url).href,
	},
	H6: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h6_coca_cherry.webp', import.meta.url).href,
	},

	// --- Pack V6 : les atlas d'animation des portraits ---
	// portraits.json porte h1,h2,h4,h5,h6 (6 poses chacun),
	// shanna.json porte h3 (8 poses). Les .webp sont a cote.
	portraitsSheet: {
		type: 'sprites',
		src: new URL('../../assets/sprites/portraits/portraits.json', import.meta.url).href,
	},
	shannaSheet: {
		type: 'sprites',
		src: new URL('../../assets/sprites/portraits/shanna.json', import.meta.url).href,
	},

	L1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l1_verifie.webp', import.meta.url).href,
	},
	L2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l2_message.webp', import.meta.url).href,
	},
	L3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l3_flamme.webp', import.meta.url).href,
	},
	L4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l4_coeur.webp', import.meta.url).href,
	},

	W: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/wild.webp', import.meta.url).href,
	},
	M: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/match_icon.webp', import.meta.url).href,
	},
	K: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_icon.webp', import.meta.url).href,
	},
	afterDarkHeartDisplay: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/afterdark_heart_display.webp', import.meta.url).href,
	},
	duelPlus2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus2.webp', import.meta.url).href,
	},
	duelPlus3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus3.webp', import.meta.url).href,
	},
	duelPlus4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus4.webp', import.meta.url).href,
	},
	duel5x: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_5x.webp', import.meta.url).href,
	},
	matchPlus3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/match_plus3.webp', import.meta.url).href,
	},
	heartBullet: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_heart_bullet.webp', import.meta.url).href,
	},
	S: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/date_scatter.webp', import.meta.url).href,
	},

	matchReveal: {
		type: 'sprite',
		src: new URL('../../assets/sprites/banners/match_reveal.webp', import.meta.url).href,
	},
	superlikeReveal: {
		type: 'sprite',
		src: new URL('../../assets/sprites/banners/superlike_reveal.webp', import.meta.url).href,
	},

	boardBackground: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_background.webp', import.meta.url).href,
	},
	boardBackgroundAfterDark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_background_after_dark.webp', import.meta.url)
			.href,
	},
	boardFrameOverlay: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_frame_overlay.webp', import.meta.url).href,
	},
	boardFrameOverlayAfterDark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_frame_overlay_after_dark.webp', import.meta.url)
			.href,
	},
	loadingScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/loading_screen.webp', import.meta.url).href,
		preload: true,
	},
	progressBar: {
		type: 'sprites',
		src: new URL('../../assets/sprites/progressBar/progressBar.json', import.meta.url).href,
		preload: true,
	},
	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/louvo_intro_screen.webp', import.meta.url).href,
	},
	speedDatingAnnounce: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/speed_dating_announce.webp', import.meta.url).href,
	},
	afterDarkAnnounce: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/after_dark_announce.webp', import.meta.url).href,
	},
	maxwinScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/maxwin.webp', import.meta.url).href,
	},
	bigwinScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/bigwin.webp', import.meta.url)
			.href,
	},
	superwinScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/superwin.webp', import.meta.url)
			.href,
	},
	megawinScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/megawin.webp', import.meta.url)
			.href,
	},
	epicwinScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/epicwin.webp', import.meta.url)
			.href,
	},
	totalWinFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/total_win_frame.webp', import.meta.url)
			.href,
	},
	bonus4ScatterScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/bonus_4_scatter_screen.webp', import.meta.url).href,
	},

	matchRevealKiss: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/match-reveal/match_reveal_sharpstop_mobile.json', import.meta.url)
			.href,
	},
	matchRevealExit: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/match-exit/match_exit_final_locked_mobile.json', import.meta.url)
			.href,
	},

	uiBottomBar: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/bottom_bar.webp', import.meta.url).href,
	},
	uiSettingsMenu: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_settings_menu.webp', import.meta.url).href,
	},
	uiBonusIcon: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_bonus_icon.webp', import.meta.url).href,
	},
	louvoCard_date: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_date.webp', import.meta.url).href,
	},
	louvoCard_match: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_match.webp', import.meta.url).href,
	},
	louvoCard_superlike: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_superlike.webp', import.meta.url).href,
	},
	louvoCard_speeddating: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_speeddating.webp', import.meta.url).href,
	},
	louvoCard_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_afterdark.webp', import.meta.url).href,
	},
	louvoConfirm_match: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_match.webp', import.meta.url).href,
	},
	louvoConfirm_superlike: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_superlike.webp', import.meta.url).href,
	},
	louvoConfirm_date: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_date.webp', import.meta.url).href,
	},
	louvoConfirm_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_afterdark.webp', import.meta.url).href,
	},
	louvoConfirm_speeddating: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_speeddating.webp', import.meta.url).href,
	},

	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
	louvoLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_logo.webp', import.meta.url).href,
	},
} as const;
