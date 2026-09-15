<script lang="ts">
	// ============================================================
	// LE R ET INSO, DE CHAQUE COTE DE LA GRILLE.        (lot 147)
	//
	// POUR TOUT ETEINDRE : PERSONNAGES = false, juste en dessous.
	// Ils disparaissent ET les 23 Mo d'atlas ne se chargent meme
	// pas. Pour desinstaller entierement, lancez a la racine :
	//     python3 desinstaller_personnages.txt
	//
	// ------------------------------------------------------------
	// POURQUOI ILS NE SONT PAS DANS L'AMBIANCE
	//
	// Ambience.svelte etire le decor avec DEUX facteurs differents,
	// un horizontal et un vertical :
	//     scale.set(canvas.width/1672, canvas.height/941)
	// Pour une image de fond c'est invisible. Un personnage, lui,
	// serait gras sur un ecran large et etire sur un ecran haut.
	//
	// On reprend donc l'etirement pour la POSITION - ils restent
	// plantes sur la terrasse peinte, quelle que soit la fenetre -
	// mais un seul facteur pour la TAILLE. Jamais deformes.
	//
	// ------------------------------------------------------------
	// POURQUOI LE CHARGEMENT EST CONDITIONNEL
	//
	// Les deux atlas pesent 23,6 Mio de memoire video. Masquer un
	// conteneur n'en libere aucun : c'est le chargement lui-meme
	// qu'il faut eviter. On decide donc AVANT de charger.
	//
	// Ce composant est pose sous {#if !showLoadingScreen} : les
	// 3,2 Mo partent apres l'ecran de chargement, jamais au milieu
	// d'un tour.
	//
	// ------------------------------------------------------------
	// L'HORLOGE
	//
	// requestAnimationFrame, pas le ticker de Pixi : meme raison
	// que pour l'ambiance, ce ticker n'existe pas toujours au
	// montage. Temps reel, donc les gestes ne s'accelerent pas
	// parce que les rouleaux vont plus vite.
	// ============================================================
	import { onDestroy } from 'svelte';
	import { getContextParent } from 'pixi-svelte';
	import { Assets, Container } from 'pixi.js';

	import * as packSide from '../pack-side';
	import { getContext } from '../game/context';
	import { dire } from '../game/journal';
	import {
		brancherPersonnages,
		debrancherPersonnages,
	} from '../game/sideCharacters.svelte';

	// --- L'INTERRUPTEUR ---
	const PERSONNAGES = true;

	// --- LES REGLAGES ---
	// Les ancres viennent du pack, dans SA toile de 1672 x 941 :
	// c'est la meme que celle du decor. y = 795 pose les pieds sur
	// la terrasse.
	const TOILE_LARGEUR = 1672;
	const TOILE_HAUTEUR = 941;
	const ANCRE_GAUCHE = { x: 240, y: 795 };
	const ANCRE_DROITE = { x: 1435, y: 795 };
	const HAUTEUR = 500;

	// --- LES REGLAGES DU DIRECTEUR ---
	// Ce sont des choix de PRESENTATION. Aucun n'a le moindre
	// effet sur les resultats du jeu, qui viennent du Math SDK.
	const REGLAGES = {
		// A partir de quel gain ils reagissent (en fois la mise).
		minWinMultiplier: 5,
		// A partir de quel gain c'est une celebration, pas un
		// simple pouce leve.
		celebrateMultiplier: 20,
		// Tours minimum entre deux reactions positives.
		//
		// Le pack met 4 par defaut, pour eviter qu'ils s'agitent
		// sans arret. Sur Louvo un gain de 5x ou plus tombe environ
		// un tour sur vingt : la protection ne protegeait de rien et
		// avalait le deuxieme gain de toute serie. A 1, ils reagissent
		// a chaque gain qui passe le seuil.
		winCooldownRounds: 1,
		// Tours d'affilee sans gain avant l'agacement.
		noWinStreak: 10,
		// Le petit geste de depit entre le 3e et le 9e tour sans
		// gain : sa chance par tour, et l'ecart minimum entre deux.
		// A 0, plus aucun geste occasionnel.
		occasionalChance: 0.12,
		occasionalCooldownRounds: 8,
	};

	// Une ligne de console par tour, qui dit POURQUOI ils ont
	// reagi ou non. Indispensable pour regler, encombrant ensuite :
	// repassez-le a false quand les valeurs vous conviendront.
	const TRACER_REACTIONS = false;

	// Sous quel cote le plus court de la fenetre on considere qu'on
	// est sur un petit ecran, et qu'on ne charge rien.
	const PETIT_ECRAN = 600;
	// Au-dessus de ce nombre d'images par seconde manquees, rien
	// n'est fait : l'horloge se contente de plafonner les sauts.
	const DELTA_MAX = 100;

	const context = getContext();
	const parentContext = getContextParent();

	// ------------------------------------------------------------
	// LE RENDEZ-VOUS AVEC SVELTE.                        (lot 148)
	//
	// addToParent n'accroche pas seulement l'objet : il enregistre
	// aussi le nettoyage a faire au demontage. Svelte n'accepte
	// d'enregistrer un nettoyage QUE pendant l'initialisation du
	// composant. Appele apres un await - le temps que 3,2 Mo
	// arrivent - il leve lifecycle_outside_component et rien ne
	// s'affiche.
	//
	// On accroche donc un conteneur VIDE tout de suite, ici, sans
	// aucun await avant. Les personnages y seront ranges plus tard
	// avec un simple addChild : du Pixi pur, qui se moque du cycle
	// de vie de Svelte.
	//
	// Ambience.svelte fait exactement pareil.
	// ------------------------------------------------------------
	const racine = new Container();
	// Ils ne prennent jamais un clic au passage, et se dessinent
	// juste au-dessus des fonds (qui sont a -4, -3 et -2).
	racine.eventMode = 'none';
	racine.zIndex = -1;
	parentContext.addToParent(racine);

	const urlLer = new URL('../../assets/side/ler.json', import.meta.url).href;
	const urlInso = new URL('../../assets/side/inso.json', import.meta.url).href;

	// Un vrai petit ecran : pointeur grossier (doigt) OU fenetre
	// etroite. Un portable a ecran tactile garde un pointeur fin,
	// il n'est donc pas pris pour un telephone.
	const surMobile = () => {
		try {
			const grossier =
				typeof window !== 'undefined' &&
				typeof window.matchMedia === 'function' &&
				window.matchMedia('(pointer: coarse)').matches;
			const petit =
				typeof window !== 'undefined' &&
				Math.min(window.innerWidth, window.innerHeight) < PETIT_ECRAN;
			return grossier || petit;
		} catch {
			return false;
		}
	};

	const modeCourant = () => {
		const palier = context.stateGame.tier;
		if (palier === 'after_dark') return 'afterDark';
		if (palier === 'speed_dating') return 'speedDating';
		return 'base';
	};

	// duo n'est PAS du $state : ce sont des objets Pixi, un proxy
	// profond de Svelte les casserait. On passe par un simple
	// drapeau pour reveiller les effets.
	let duo: any = null;
	let pret = $state(false);
	let horloge = 0;
	let dernier = 0;
	let image = 0;
	let vivant = true;

	const pas = (maintenant: number) => {
		if (!vivant) return;
		image = requestAnimationFrame(pas);
		if (!duo) return;
		const delta = dernier ? Math.min(maintenant - dernier, DELTA_MAX) : 16.7;
		dernier = maintenant;
		horloge += delta;
		try {
			duo.seek(horloge);
		} catch (erreur) {
			console.warn('[louvo] personnages : seek', erreur);
			vivant = false;
		}
	};

	const installer = async () => {
		if (!PERSONNAGES) return;
		if (surMobile()) {
			dire('[louvo] personnages : petit ecran, aucun atlas charge');
			return;
		}
		try {
			const [ler, inso] = await Promise.all([
				Assets.load(urlLer),
				Assets.load(urlInso),
			]);
			if (!vivant) return;
			duo = packSide.createSideCharacters(
				{ ler, inso },
				{ mode: modeCourant(), isMobile: false, reducedMotion: false },
			);
			// Le conteneur est deja accroche depuis le montage : ici on
			// ne fait que le remplir.
			racine.addChild(duo.root);
			brancherPersonnages(
				duo,
				packSide.createSideReactionDirector(duo, REGLAGES),
				() => horloge,
				TRACER_REACTIONS,
			);
			pret = true;
			image = requestAnimationFrame(pas);
			// Les atlas sont la. La POSITION, elle, n'est pas encore
			// calculee a cet instant : elle se dit plus bas, une fois
			// la pose faite. Annoncer des coordonnees avant de les
			// avoir calculees, c'est pire que ne rien annoncer.
			dire('[louvo] personnages : atlas charges');
		} catch (erreur) {
			// Un decor rate ne peut pas eteindre le jeu.
			console.warn('[louvo] personnages : installation abandonnee', erreur);
			duo = null;
		}
	};

	installer();

	// --- La pose, refaite a chaque changement de fenetre ---
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	let poseDite = false;
	$effect(() => {
		if (!pret || !duo) return;
		const fx = canvas.width / TOILE_LARGEUR;
		const fy = canvas.height / TOILE_HAUTEUR;
		try {
			duo.layout({
				left: { x: ANCRE_GAUCHE.x * fx, y: ANCRE_GAUCHE.y * fy },
				right: { x: ANCRE_DROITE.x * fx, y: ANCRE_DROITE.y * fy },
				// UN SEUL facteur : la taille suit la hauteur du decor,
				// jamais sa largeur. C'est ce qui evite la deformation.
				height: HAUTEUR * fy,
			});
			// Maintenant seulement, les vraies valeurs.
			if (!poseDite) {
				poseDite = true;
				dire(
					'[louvo] personnages en place : ' +
						JSON.stringify({
							mode: modeCourant(),
							visible: racine.visible && duo.root.visible,
							fenetre: Math.round(canvas.width) + 'x' + Math.round(canvas.height),
							gauche: Math.round(duo.ler.x) + ',' + Math.round(duo.ler.y),
							droite: Math.round(duo.inso.x) + ',' + Math.round(duo.inso.y),
							echelle: duo.ler.scale.x.toFixed(3),
						}),
				);
			}
		} catch (erreur) {
			console.warn('[louvo] personnages : pose', erreur);
		}
	});

	// --- Le mode : ils se cachent en After Dark et sur petit ecran ---
	const palier = $derived(context.stateGame.tier);
	$effect(() => {
		if (!pret || !duo) return;
		void palier;
		void canvas;
		try {
			duo.setContext({ mode: modeCourant(), isMobile: surMobile() });
		} catch (erreur) {
			console.warn('[louvo] personnages : contexte', erreur);
		}
	});

	onDestroy(() => {
		vivant = false;
		if (image) cancelAnimationFrame(image);
		debrancherPersonnages();
		try {
			if (duo) {
				racine.removeChild(duo.root);
				duo.destroy();
			}
		} catch {
			// rien : on part de toute facon
		}
		duo = null;
	});
</script>
