path = "apps/louvo/src/components/LouvoIntroScreen.svelte"
with open(path, "r") as f:
    content = f.read()

old_y = """	const TITLE_Y_FRAC = 0.4;
	const BODY_Y_FRAC = 0.7333;"""
new_y = """	const TITLE_Y_FRAC = 0.371;
	const BODY_Y_FRAC = 0.7725;"""

old_text = "'The MATCH and SUPER LIKE reels are back, and this time they bring multipliers and a rain of wilds!'"
new_text = "'The MATCH and SUPER LIKE reels bring multipliers and a rain of wilds!'"

missing = [n for n, o in [("y", old_y), ("text", old_text)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_y, new_y, 1)
    content = content.replace(old_text, new_text, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : titres remontes, descriptions descendues (mesures calibrees sur le rendu reel), texte 'are back' retire.")
