path = "apps/louvo/src/components/MatchDuelClash.svelte"
with open(path, "r") as f:
    content = f.read()

old_consts = """	const SIDE_OFFSET = 28;
	const FONT_SIZE = 44;
	const WINNER_FONT_SIZE = 60;"""
new_consts = """	const SIDE_OFFSET = 28;
	const FONT_SIZE = 44;
	const WINNER_FONT_SIZE = 60;
	const Y_POSITION = 114; // pile entre le milieu (0) et le bas de la banniere
	const TEXT_Z_INDEX = 20; // toujours au-dessus de l'animation bisou/rupture qui suit"""

old_markup = """{#if !showWinnerOnly}
	<BitmapText
		anchor={0.5}
		x={leftX}
		scale={leftScale}
		alpha={leftAlpha}
		text={`x${props.duelValues[0]}`}
		style={{ fontFamily: 'gold', fontSize: FONT_SIZE }}
	/>
	<BitmapText
		anchor={0.5}
		x={rightX}
		scale={rightScale}
		alpha={rightAlpha}
		text={`x${props.duelValues[1]}`}
		style={{ fontFamily: 'gold', fontSize: FONT_SIZE }}
	/>
{:else}
	<BitmapText
		anchor={0.5}
		text={`x${props.winner}`}
		style={{ fontFamily: 'gold', fontSize: WINNER_FONT_SIZE }}
	/>
{/if}"""
new_markup = """{#if !showWinnerOnly}
	<BitmapText
		anchor={0.5}
		x={leftX}
		y={Y_POSITION}
		scale={leftScale}
		alpha={leftAlpha}
		zIndex={TEXT_Z_INDEX}
		text={`x${props.duelValues[0]}`}
		style={{ fontFamily: 'gold', fontSize: FONT_SIZE }}
	/>
	<BitmapText
		anchor={0.5}
		x={rightX}
		y={Y_POSITION}
		scale={rightScale}
		alpha={rightAlpha}
		zIndex={TEXT_Z_INDEX}
		text={`x${props.duelValues[1]}`}
		style={{ fontFamily: 'gold', fontSize: FONT_SIZE }}
	/>
{:else}
	<BitmapText
		anchor={0.5}
		y={Y_POSITION}
		zIndex={TEXT_Z_INDEX}
		text={`x${props.winner}`}
		style={{ fontFamily: 'gold', fontSize: WINNER_FONT_SIZE }}
	/>
{/if}"""

missing = [n for n, o in [("consts", old_consts), ("markup", old_markup)] if o not in content]
if missing:
    print("ERREUR : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_consts, new_consts, 1)
    content = content.replace(old_markup, new_markup, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : Y_POSITION=114 + zIndex appliques sur les 3 textes.")

echo_check = content.count("Y_POSITION") if 'content' in dir() else 0
