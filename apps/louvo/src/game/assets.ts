export default {
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
	introScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/intro_screen.png', import.meta.url).href,
	},
	loadingScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/loading_screen.png', import.meta.url).href,
	},
	speedDatingAnnounce: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/speed_dating_announce.png', import.meta.url).href,
	},
	afterDarkAnnounce: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/after_dark_announce.png', import.meta.url).href,
	},
	bonus4ScatterScreen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/screens/bonus_4_scatter_screen.png', import.meta.url).href,
	},

	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;
