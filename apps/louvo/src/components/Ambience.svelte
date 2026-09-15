<script lang="ts">
	// ============================================================
	// L'AMBIANCE : le fond anime du pack V6.            (lot 135)
	//
	// createAmbience dessine ses bougies, ses fenetres de ville et
	// ses coeurs de ciel a des coordonnees FIXES dans une toile de
	// 1672 x 941. Background.svelte, lui, etire l'image sur TOUT le
	// canvas sans garder le ratio. Ce composant reproduit cet
	// etirement a l'identique - c'est la seule chose qui garantit
	// que les lueurs tombent sur les bougies.
	//
	// L'HORLOGE (lot 133). requestAnimationFrame, pas le ticker de
	// Pixi : le fond est le premier element de la scene et ce ticker
	// n'existe pas toujours a ce moment-la. Temps reel, donc le
	// decor ne s'accelere pas parce que les rouleaux vont plus vite.
	//
	// LE GEL (lot 134). Le module du pack fait, dans seek() :
	//     const t = reducedMotion ? 0 : ms/1000;
	// Si le systeme demande "moins d'animations", le decor est fige
	// sur sa premiere image POUR TOUJOURS. Le reste du jeu ignore ce
	// reglage : on l'ignore ici aussi.
	//
	// LE CIEL (lot 135). Pixi lit les attributs du shader a l'expres-
	// sion reguliere, pas au compilateur. Si la signature de
	// mainVertex n'est pas dans SA forme a lui, il fabrique un
	// pipeline WebGPU sans attribut et TOUT l'ecran devient noir. On
	// relit donc la signature AVANT de brancher le ciel. Refusee :
	// pas de ciel, mais le reste du decor tourne et le jeu s'affiche.
	//
	// SECURITE : si l'ambiance ne peut pas etre construite, on
	// affiche l'image fixe, exactement comme avant. Un decor rate ne
	// peut pas eteindre le jeu.
	// ============================================================
	import { onDestroy } from 'svelte';
	import { Sprite, getContextApp, getContextParent } from 'pixi-svelte';
	import * as pack from '../pack';
	import { getContext } from '../game/context';

	import { dire } from '../game/journal';
	type Props = {
		/** 'base' ou 'afterDark' : choisit le jeu de points du pack. */
		mode: 'base' | 'afterDark';
		/** La cle de l'image de fond dans assets.ts. */
		cle: string;
		/** Faux quand ce fond est en train de disparaitre. */
		actif?: boolean;
	};
	const props: Props = $props();

	// Les dimensions de la toile dans laquelle le pack a releve ses
	// points. A ne pas toucher : elles viennent des images elles-memes.
	const TOILE_LARGEUR = 1672;
	const TOILE_HAUTEUR = 941;

	// Le ciel qui ondule. false le coupe sans rien casser d'autre :
	// les bougies, les fenetres et la terrasse continuent.
	const CIEL_ANIME = true;

	// Faut-il tenir compte de "reduire les animations" du systeme ?
	// false : non, le decor tourne pour tout le monde - comme le
	//         reste du jeu, qui ne lit pas ce reglage.
	// true  : oui, mais AU RALENTI, jamais gele.
	const RESPECTER_SOBRIETE = false;
	const VITESSE_SOBRE = 0.4;

	// Force du battement des bougies, des fenetres et de la terrasse.
	// 1 = exactement ce que le pack a prevu. 1.5 ou 2 creusent l'ecart
	// entre le haut et le bas du battement SANS eclaircir le decor.
	const INTENSITE = 1;

	// Combien de temps l'ambiance invisible reste dessinee, le temps
	// que le fondu d'une seconde se termine.
	const FONDU_MS = 1200;
	// Quand la ligne de bilan part dans la console.
	const BILAN_MS = 4000;

	const context = getContext();
	const contextApp = getContextApp();
	const parentContext = getContextParent();

	// --- Le carnet de bord ---
	// Une seule ligne dans la console, 4 s apres le lancement, qui dit
	// si l'ambiance tourne. Aucun cout : quelques nombres.
	const fiche: any = {
		api: false,
		cielVerifie: false,
		ciel: false,
		filtre: false,
		cielTemps: 0,
		enfants: 0,
		pas: 0,
		secondes: 0,
		lueurMin: 9,
		lueurMax: -9,
		sobre: false,
		vitesse: 1,
		attache: false,
		dessine: null,
		echelle: '',
		echecs: [] as string[],
	};

	if (typeof window !== 'undefined') {
		const w = window as any;
		if (!w.__louvoAmbiance) {
			w.__louvoAmbiance = {};
			setTimeout(() => {
				try {
					dire(
						'[louvo] bilan ambiance : ' +
							JSON.stringify(w.__louvoAmbiance, (_c, v) =>
								typeof v === 'number' ? Math.round(v * 100) / 100 : v,
							),
					);
				} catch (erreur) {
					dire('[louvo] bilan ambiance : illisible', erreur);
				}
			}, BILAN_MS);
		}
		w.__louvoAmbiance[props.mode] = fiche;
	}

	const noter = (m: string) => {
		if (fiche.echecs.length < 4) fiche.echecs.push(m);
	};

	// Le systeme demande-t-il moins d'animations ? On le note, mais
	// on ne s'en sert que si RESPECTER_SOBRIETE est vrai - et meme
	// alors, c'est un ralenti, pas un gel.
	const sobre = (() => {
		try {
			return (
				typeof window !== 'undefined' &&
				typeof window.matchMedia === 'function' &&
				window.matchMedia('(prefers-reduced-motion: reduce)').matches
			);
		} catch {
			return false;
		}
	})();
	const VITESSE = RESPECTER_SOBRIETE && sobre ? VITESSE_SOBRE : 1;
	fiche.sobre = sobre;
	fiche.vitesse = VITESSE;

	// Combien de bougies, combien de fenetres : sert au reglage
	// d'intensite, qui doit savoir quel enfant est quoi.
	const POINTS = (pack as any)?.AMBIENCE_POINTS?.[props.mode];
	const N_BOUGIES = POINTS?.candles?.length ?? 0;
	const N_FENETRES = POINTS?.city?.length ?? 0;

	// --- LE CONTROLE AVANT VOL DU CIEL ---
	// Pixi cherche les attributs du shader entre "fn mainVertex" et
	// la fleche de retour, a l'expression reguliere. Il lui faut une
	// virgule apres le type. Si on ne la lui donne pas, il construit
	// un pipeline WebGPU sans aucun attribut, le GPU refuse tout et
	// l'ecran devient noir. On verifie ici, avant de brancher quoi
	// que ce soit : refuse, on se passe simplement du ciel.
	const cielUtilisable = () => {
		if (!CIEL_ANIME) return false;
		try {
			const source = (pack as any)?.createSkyWgsl?.(POINTS?.hearts ?? []);
			if (typeof source !== 'string') return false;
			const debut = source.indexOf('fn mainVertex');
			if (debut === -1) return false;
			const fleche = source.indexOf('->', debut);
			if (fleche === -1) return false;
			const signature = source.substring(debut, fleche);
			return /@location\(\s*0\s*\)\s+aPosition\s*:\s*vec2<f32>\s*,/.test(
				signature,
			);
		} catch {
			return false;
		}
	};
	const CIEL_OK = cielUtilisable();
	fiche.cielVerifie = CIEL_OK;
	if (CIEL_ANIME && !CIEL_OK) {
		noter('ciel refuse au controle : signature du shader');
		console.warn(
			'[louvo] ambiance : ciel refuse au controle, signature du shader',
		);
	}

	const fabriquer = () => {
		const texture = (contextApp as any)?.stateApp?.loadedAssets?.[props.cle];
		if (!texture) {
			noter('image absente : ' + props.cle);
			console.warn('[louvo] ambiance : image absente', props.cle);
			return null;
		}
		// D'abord avec le ciel s'il a passe le controle, puis sans,
		// puis rien du tout.
		// reducedMotion reste a false EN DUR : c'est le drapeau qui
		// forcait le temps a zero dans seek(). Le ralenti eventuel se
		// fait chez nous, sur l'horloge.
		for (const ciel of [CIEL_OK, false]) {
			try {
				const a = pack.createAmbience(texture, {
					mode: props.mode,
					skyMotion: ciel,
					reducedMotion: false,
				});
				a.seek(0);
				fiche.ciel = !!ciel;
				fiche.filtre = !!(a as any).filter;
				if (!ciel && CIEL_OK) {
					noter('ciel desactive : construction refusee');
					console.warn('[louvo] ambiance : ciel desactive');
				}
				return a;
			} catch (erreur) {
				noter(String(erreur).slice(0, 90));
				console.warn('[louvo] ambiance :', props.mode, erreur);
			}
		}
		return null;
	};

	const api = fabriquer();
	if (api) {
		parentContext.addToParent(api.root);
		fiche.api = true;
		fiche.enfants = api.root.children.length;
	}

	// --- L'etirement, copie sur Background.svelte ---
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	$effect(() => {
		if (!api) return;
		api.root.position.set(0, 0);
		api.root.scale.set(
			canvas.width / TOILE_LARGEUR,
			canvas.height / TOILE_HAUTEUR,
		);
		fiche.echelle =
			api.root.scale.x.toFixed(3) + ' x ' + api.root.scale.y.toFixed(3);
	});

	// --- Le bouton de reglage ---
	// Les enfants de l'ambiance, dans l'ordre ou le pack les ajoute :
	// [0] l'image de fond, puis les bougies, puis les fenetres, puis
	// le halo de la terrasse. On creuse l'ecart autour de la valeur
	// moyenne de chacun : plus contraste, pas plus lumineux.
	const amplifier = () => {
		if (INTENSITE === 1 || !api) return;
		const enfants = api.root.children;
		const ajuster = (n: any, moyenne: number) => {
			if (!n) return;
			n.alpha = Math.max(
				0,
				Math.min(1, moyenne + (n.alpha - moyenne) * INTENSITE),
			);
		};
		let i = 1;
		for (let k = 0; k < N_BOUGIES && i < enfants.length; k += 1) {
			ajuster(enfants[i], 0.6);
			i += 1;
		}
		for (let k = 0; k < N_FENETRES && i < enfants.length; k += 1) {
			ajuster(enfants[i], 0.48);
			i += 1;
		}
		if (i < enfants.length) ajuster(enfants[i], 0.7);
	};

	// --- L'horloge du navigateur ---
	let horloge = 0;
	let dernier = 0;
	let image = 0;
	let vivant = true;
	let extinction: ReturnType<typeof setTimeout> | null = null;

	const pas = (maintenant: number) => {
		if (!vivant) return;
		image = requestAnimationFrame(pas);
		if (!api) return;
		// Un onglet remis au premier plan peut rendre un delta enorme :
		// on le plafonne pour que le decor ne fasse pas un bond.
		const delta = dernier ? Math.min(maintenant - dernier, 100) : 16.7;
		dernier = maintenant;
		horloge += delta * VITESSE;
		try {
			api.seek(horloge);
			amplifier();
			fiche.pas += 1;
			fiche.secondes = horloge / 1000;
			const lueur = api.root.children[1];
			if (lueur) {
				if (lueur.alpha < fiche.lueurMin) fiche.lueurMin = lueur.alpha;
				if (lueur.alpha > fiche.lueurMax) fiche.lueurMax = lueur.alpha;
			}
			fiche.cielTemps =
				(api as any).filter?.resources?.skyUniforms?.uniforms?.uTime ?? 0;
			fiche.attache = !!api.root.parent;
			fiche.dessine = api.root.renderable && api.root.visible;
		} catch (erreur) {
			noter('seek : ' + String(erreur).slice(0, 80));
			console.warn('[louvo] ambiance : seek', props.mode, erreur);
			vivant = false;
		}
	};

	if (typeof requestAnimationFrame === 'function') {
		image = requestAnimationFrame(pas);
	} else {
		noter('pas de requestAnimationFrame');
	}

	// Le fond cache cesse d'etre dessine une fois le fondu fini.
	$effect(() => {
		if (!api) return;
		if (extinction) {
			clearTimeout(extinction);
			extinction = null;
		}
		if (props.actif === false) {
			extinction = setTimeout(() => {
				if (api) api.root.renderable = false;
			}, FONDU_MS);
		} else {
			api.root.renderable = true;
		}
	});

	onDestroy(() => {
		vivant = false;
		if (image && typeof cancelAnimationFrame === 'function') {
			cancelAnimationFrame(image);
		}
		if (extinction) clearTimeout(extinction);
		try {
			api?.destroy?.();
		} catch {
			/* on nettoie au mieux */
		}
	});
</script>

{#if !api}
	<!-- Repli : l'image fixe, exactement comme avant le pack. -->
	<Sprite
		key={props.cle}
		anchor={0.5}
		x={canvas.width * 0.5}
		y={canvas.height * 0.5}
		width={canvas.width}
		height={canvas.height}
	/>
{/if}
