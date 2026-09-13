<script lang="ts">
	// ============================================================
	// La passerelle entre le pack V6 et pixi-svelte.
	//
	// Les modules du pack rendent un objet Pixi brut :
	//     { root, duration, seek(ms) }
	// Ce composant l'accroche a l'arbre du jeu, exactement comme
	// le fait Container.svelte de pixi-svelte, puis appelle seek()
	// a chaque image en suivant le turbo.
	//
	// SECURITE : si l'atlas n'est pas la, fabriquer() renvoie null
	// et le symbole retombe sur son image fixe. Un atlas manquant
	// ne peut pas eteindre le jeu.
	// ============================================================
	import { onDestroy } from 'svelte';
	import { getContextApp, getContextParent } from 'pixi-svelte';
	import { SYMBOL_WIDTH, SYMBOL_HEIGHT } from '../game/constants';
	import { getSymbolInfo } from '../game/utils';
	import { stateGame } from '../game/stateGame.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import * as pack from '../pack';
	import * as PIXI from 'pixi.js';
	import assets from '../game/assets';

	// --- Bilan, ecrit une seule fois dans la console ---
	const bilan = (() => {
		const g = globalThis as any;
		if (!g.__louvoBilan) {
			g.__louvoBilan = {
				montes: 0,
				animees: 0,
				replis: 0,
				horloge: false,
				images: 0,
				echecs: [] as string[],
			};
			setTimeout(() => {
				console.log('[louvo] bilan animations :',
					JSON.stringify(g.__louvoBilan));
			}, 4000);
		}
		return g.__louvoBilan;
	})();

	const noter = (quoi: string) => {
		if (bilan.echecs.length < 8 && !bilan.echecs.includes(quoi)) {
			bilan.echecs.push(quoi);
		}
	};
	import { stateBetDerived } from 'state-shared';
	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		loop?: boolean;
		oncomplete?: () => void;
		zIndex?: number;
	};
	const props: Props = $props();

	// Meme valeur que SymbolSprite : le cadre After Dark est plus grand.
	const AFTER_DARK_SIZE_SCALE = 1.02;

	const contextApp = getContextApp();
	const parentContext = getContextParent();

	const nom = (props.symbolInfo as { pack?: string }).pack ?? '';

	// --- 1. Recuperer une feuille d'images, si elle est bien chargee ---
	// Retrouve la feuille d'images d'un atlas, quelle que soit la forme
	// sous laquelle le chargeur l'a rangee.
	//
	// Le pack a besoin d'un acces PAR NOM : sheet.textures['h1-00'].
	// Or le SDK range les atlas type 'sprites' sous forme de TABLEAU
	// ordonne (cf. SpriteSheet.svelte : `'length' in textures`), ou les
	// noms sont perdus. D'ou le recours au cache de Pixi : le fichier y
	// est deja charge, et la Spritesheet y est intacte.
	const duCache = (k: string) => {
		try {
			return (PIXI.Assets.cache as any)?.has?.(k)
				? (PIXI.Assets.cache as any).get(k)
				: undefined;
		} catch {
			return undefined;
		}
	};

	const feuille = (cle: string, prefixe: string) => {
		const premiere = prefixe + '-00';
		const valide = (f: any) => (f?.textures?.[premiere] ? f : null);
		const brut = (contextApp as any)?.stateApp?.loadedAssets?.[cle];

		// 0. LE CAS REEL. assetLoad.ts, pour type 'sprites', fait
		//    `rawAsset.textures` sans enveloppe : le chargeur REPAND les
		//    images dans loadedAssets, chacune sous son propre nom.
		//    loadedAssets['h1-00'] existe ; loadedAssets['portraitsSheet']
		//    n'existe pas. On teste donc ca en premier.
		const tous = (contextApp as any)?.stateApp?.loadedAssets ?? {};
		if (tous[premiere]) {
			const repandu: Record<string, unknown> = {};
			for (let i = 0; i < 12; i += 1) {
				const nomFrame = prefixe + '-' + String(i).padStart(2, '0');
				if (tous[nomFrame]) repandu[nomFrame] = tous[nomFrame];
			}
			return { textures: repandu };
		}

		// 1. la Spritesheet telle quelle
		let f = valide(brut);
		if (f) return f;
		// 2. un objet qui l'enveloppe
		f = valide(brut?.spritesheet ?? brut?.spriteSheet);
		if (f) return f;
		// 3. une table de textures nue
		if (brut?.[premiere]) return { textures: brut };

		// 4. le cache de Pixi, par l'URL declaree dans assets.ts
		const src = (assets as any)?.[cle]?.src;
		if (typeof src === 'string') {
			f = valide(duCache(src));
			if (f) return f;
		}

		// 5. le cache de Pixi, image par image : le lecteur d'atlas y
		//    depose chaque frame sous son propre nom.
		const table: Record<string, unknown> = {};
		for (let i = 0; i < 12; i += 1) {
			const nomFrame = prefixe + '-' + String(i).padStart(2, '0');
			const t = duCache(nomFrame);
			if (t) table[nomFrame] = t;
		}
		if (table[premiere]) return { textures: table };

		// Les cinq ont echoue : on dit sous quelle forme c'etait range,
		// plutot que de retomber en silence sur l'image fixe.
		console.warn(
			'[louvo] atlas introuvable :',
			cle,
			premiere,
			'range sous :',
			brut === undefined ? 'rien' : Object.prototype.toString.call(brut),
			Array.isArray(brut)
				? 'tableau de ' + brut.length
				: Object.keys(brut ?? {}).slice(0, 8),
		);
		return null;
	};

	// --- 2. Fabriquer l'animation demandee ---
	// background: false, TOUJOURS. Les fonctions du pack savent dessiner
	// une carte creme opaque derriere le symbole ; les images de repos
	// livrees, elles, n'en ont pas (verifie : h1_le_r.webp est identique
	// au pixel pres a la frame h1-00 de l'atlas, coins transparents
	// compris). Laisser la carte ferait surgir un rectangle creme a
	// chaque atterrissage.
	const SANS_CARTE = { background: false };

	const fabriquer = () => {
		try {
			if (['h1', 'h2', 'h4', 'h5', 'h6'].includes(nom)) {
				const f = feuille('portraitsSheet', nom);
				return f ? pack.createPortraitAnimation(f, nom, SANS_CARTE) : null;
			}
			if (nom === 'h3') {
				const f = feuille('shannaSheet', 'shanna');
				return f ? pack.createShannaAnimation(f, SANS_CARTE) : null;
			}
			if (['verified', 'message', 'flame', 'heart'].includes(nom)) {
				return pack.createLowAnimation(nom, SANS_CARTE);
			}
			if (nom === 'wild' || nom === 'date') {
				return pack.createSpecialAnimation(nom, SANS_CARTE);
			}
		} catch (erreur) {
			noter('erreur:' + nom + ':' + String(erreur).slice(0, 80));
			console.warn('[louvo] animation du pack indisponible :', nom, erreur);
		}
		return null;
	};

	const api = fabriquer();
	bilan.montes += 1;
	if (api) {
		bilan.animees += 1;
		parentContext.addToParent(api.root);
	} else {
		bilan.replis += 1;
		if (nom) noter('repli:' + nom);
	}

	// --- 3. Placement ---
	// Le pack dessine dans une boite 116x91 posee en haut a gauche ;
	// le jeu, lui, donne le CENTRE de la case. D'ou la demi-taille.
	const echelleTier = $derived(stateGame.tier === 'after_dark' ? AFTER_DARK_SIZE_SCALE : 1);
	const ex = $derived(props.symbolInfo.sizeRatios.width * echelleTier);
	const ey = $derived(props.symbolInfo.sizeRatios.height * echelleTier);

	$effect(() => {
		if (!api) return;
		api.root.scale.set(ex, ey);
		api.root.position.set(
			(props.x ?? 0) - (SYMBOL_WIDTH * ex) / 2,
			(props.y ?? 0) - (SYMBOL_HEIGHT * ey) / 2,
		);
		api.root.zIndex = props.zIndex ?? 0;
	});

	// --- 4. L'horloge ---
	let horloge = 0;
	let fini = false;
	const ticker = (contextApp as any)?.stateApp?.pixiApplication?.ticker;

	const pas = () => {
		if (!api || fini) return;
		const vitesse = stateBetDerived.timeScale();
		horloge += (ticker?.deltaMS ?? 16.7) * (vitesse > 0 ? vitesse : 1);
		if (horloge >= api.duration) {
			if (props.loop) {
				horloge %= api.duration;
			} else {
				horloge = api.duration;
				// Fini : on arrete de redessiner. Plus rien ne bouge, donc
				// plus rien ne coute - important avec 25 cases a l'ecran.
				fini = true;
				// L'animation d'atterrissage est allee au bout : c'est
				// MAINTENANT qu'on previent, pas au montage.
				prevenir();
			}
		}
		api.seek(horloge);
		bilan.images += 1;
	};

	if (api && ticker) {
		bilan.horloge = true;
		ticker.add(pas);
	} else if (api && !ticker) {
		noter('horloge introuvable');
	}

	// Si l'etat repasse en boucle apres la fin, on repart.
	$effect(() => {
		if (props.loop) fini = false;
	});

	// QUAND PREVENIR LE JEU QUE C'EST FINI
	//
	// ReelSymbol.svelte fait ceci, a la reception de oncomplete :
	//     if (symbolState === 'win')  reelSymbol.oncomplete();
	//     if (symbolState === 'land') reelSymbol.symbolState = 'static';
	//
	// L'image fixe previent des son montage. A l'atterrissage, l'etat
	// repassait donc a 'static' dans la foulee, SYMBOL_INFO_MAP renvoyait
	// de nouveau l'image fixe, et cette passerelle etait detruite AVANT
	// d'avoir dessine une seule image. C'est la raison pour laquelle
	// aucun symbole ne s'animait.
	//
	// Deux cas, et ils sont differents :
	//   'win'  -> on previent TOUT DE SUITE : ReelSymbol appelle alors
	//             reelSymbol.oncomplete(), que la presentation des gains
	//             attend. La retenir bloquerait le tour.
	//   'land' -> on previent A LA FIN de l'animation. Rien n'attend ce
	//             signal, donc le retarder ne bloque rien, et ca laisse
	//             l'animation se jouer.
	//
	// En repli (api absente) c'est SymbolSprite qui previent : sans ce
	// garde-fou l'appel partirait deux fois.
	let prevenu = false;
	const prevenir = () => {
		if (prevenu) return;
		prevenu = true;
		props.oncomplete?.();
	};

	$effect(() => {
		props.symbolInfo;
		if (api && props.loop) prevenir();
	});

	onDestroy(() => {
		if (ticker) ticker.remove(pas);
		try {
			if (api && typeof api.destroy === 'function') api.destroy();
			else api?.root?.destroy?.({ children: true });
		} catch {
			/* rien : on nettoie au mieux */
		}
	});
</script>

{#if !api}
	<!-- Atlas absent ou animation inconnue : l'image fixe, comme avant.
	     C'est elle qui appelle oncomplete dans ce cas - voir plus haut. -->
	<SymbolSprite
		symbolInfo={props.symbolInfo}
		x={props.x}
		y={props.y}
		oncomplete={props.oncomplete}
		zIndex={props.zIndex}
	/>
{/if}
