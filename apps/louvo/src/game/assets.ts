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
	anticipation: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/anticipation/anticipation.webp', import.meta.url).href,
			atlas: new URL('../../assets/spines/anticipation/anticipation.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/anticipation/anticipation.json', import.meta.url).href,
		},
	},
	bigwin: {
		type: 'spine',
		src: {
			img: new URL('../../assets/spines/bigwin/big_wins.webp', import.meta.url).href,
			atlas: new URL('../../assets/spines/bigwin/big_wins.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/bigwin/mm_bigwin.json', import.meta.url).href,
		},
	},
	H1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h1_le_r.png', import.meta.url).href,
	},
	H2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h2_inso.png', import.meta.url).href,
	},
	H3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h3_shanna.png', import.meta.url).href,
	},
	H4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h4_manu.png', import.meta.url).href,
	},
	H5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h5_indigo.png', import.meta.url).href,
	},
	H6: {
		type: 'sprite',
		src: new URL('../../assets/sprites/portraits/h6_coca_cherry.png', import.meta.url).href,
	},

	L1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l1_verifie.png', import.meta.url).href,
	},
	L2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l2_message.png', import.meta.url).href,
	},
	L3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l3_flamme.png', import.meta.url).href,
	},
	L4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/basic-symbols/l4_coeur.png', import.meta.url).href,
	},

	W: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/wild.png', import.meta.url).href,
	},
	M: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/match_icon.png', import.meta.url).href,
	},
	K: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_icon.png', import.meta.url).href,
	},
	afterDarkHeartDisplay: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/afterdark_heart_display.png', import.meta.url).href,
	},
	duelPlus2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus2.png', import.meta.url).href,
	},
	duelPlus3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus3.png', import.meta.url).href,
	},
	duelPlus4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_plus4.png', import.meta.url).href,
	},
	duel5x: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/duel_5x.png', import.meta.url).href,
	},
	matchPlus3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/after-dark/match_plus3.png', import.meta.url).href,
	},
	heartBullet: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/superlike_heart_bullet.png', import.meta.url).href,
	},
	S: {
		type: 'sprite',
		src: new URL('../../assets/sprites/special/date_scatter.png', import.meta.url).href,
	},

	matchReveal: {
		type: 'sprite',
		src: new URL('../../assets/sprites/banners/match_reveal.png', import.meta.url).href,
	},
	superlikeReveal: {
		type: 'sprite',
		src: new URL('../../assets/sprites/banners/superlike_reveal.png', import.meta.url).href,
	},

	boardBackground: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_background.png', import.meta.url).href,
	},
	boardBackgroundAfterDark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_background_after_dark.png', import.meta.url)
			.href,
	},
	boardFrameOverlay: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_frame_overlay.png', import.meta.url).href,
	},
	boardFrameOverlayAfterDark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/board_frame_overlay_after_dark.png', import.meta.url)
			.href,
	},
	loadingScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/loading_screen.png', import.meta.url).href,
		preload: true,
	},
	progressBar: {
		type: 'sprites',
		src: new URL('../../assets/sprites/progressBar/progressBar.json', import.meta.url).href,
		preload: true,
	},
	louvoIntroScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/louvo_intro_screen.png', import.meta.url).href,
	},
	speedDatingAnnounce: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/speed_dating_announce.png', import.meta.url).href,
	},
	afterDarkAnnounce: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/after_dark_announce.png', import.meta.url).href,
	},
	maxwinScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/maxwin.png', import.meta.url).href,
	},
	bonus4ScatterScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/bonus_4_scatter_screen.png', import.meta.url).href,
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
		src: new URL('../../assets/sprites/ui/bottom_bar.png', import.meta.url).href,
	},
	uiSettingsMenu: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_settings_menu.png', import.meta.url).href,
	},
	uiBonusIcon: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_bonus_icon.png', import.meta.url).href,
	},
	louvoCard_date: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_date.png', import.meta.url).href,
	},
	louvoCard_match: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_match.png', import.meta.url).href,
	},
	louvoCard_superlike: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_superlike.png', import.meta.url).href,
	},
	louvoCard_speeddating: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_speeddating.png', import.meta.url).href,
	},
	louvoCard_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_card_afterdark.png', import.meta.url).href,
	},
	louvoConfirm_match: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_match.png', import.meta.url).href,
	},
	louvoConfirm_superlike: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_superlike.png', import.meta.url).href,
	},
	louvoConfirm_date: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_date.png', import.meta.url).href,
	},
	louvoConfirm_afterdark: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_afterdark.png', import.meta.url).href,
	},
	louvoConfirm_speeddating: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_confirm_speeddating.png', import.meta.url).href,
	},

	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
	louvoLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/ui/louvo_logo.png', import.meta.url).href,
	},
} as const;
