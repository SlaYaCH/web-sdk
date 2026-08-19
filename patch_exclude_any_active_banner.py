path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = """	// Securite : exclut toute position ciblee sur la colonne ou se trouve
	// la banniere elle-meme (ne devrait jamais arriver cote Math SDK, mais
	// un coeur ne doit JAMAIS atterrir sur l'emplacement de la banniere).
	const positions = (props.positions ?? []).filter((p) => p.reelIndex !== props.reelIndex);"""
new = """	// Securite : exclut toute position ciblee sur la colonne de la banniere
	// Super Like elle-meme OU sur la colonne d'une AUTRE banniere active en
	// meme temps (ex: Match Duel sur un autre rouleau du meme spin) - un
	// coeur ne doit JAMAIS atterrir sur une case occupee par une banniere.
	const positions = (props.positions ?? []).filter(
		(p) => p.reelIndex !== props.reelIndex && p.reelIndex !== context.stateGame.activeBannerReelIndex,
	);"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : coeurs excluent maintenant aussi la colonne de toute AUTRE banniere active simultanement.")
