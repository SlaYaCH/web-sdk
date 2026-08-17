path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

RULES_HTML = '''<div class="louvo-rules">
	<h2>ABOUT THE GAME</h2>
	<p>Welcome to Louvo! Swipe into a 5-reel, 5-row grid packed with 19 paylines, and see who really matches. The maximum win of 15,000x your bet can be hit in any game mode.</p>

	<h2>FEATURES</h2>

	<h3>THE MATCH DUEL</h3>
	<p>When two MATCH symbols land, they face off in a duel. Each side is dealt a multiplier, and only one wins the exchange, either could take it. The surviving multiplier is applied to the win.</p>

	<h3>SUPER LIKE</h3>
	<p>The SUPER LIKE symbol sends out between 1 and 6 Wilds to random empty positions on the grid, each carrying the same multiplier drawn for the Super Like itself.</p>

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
	<p><strong>WILD</strong> substitutes for all symbols on the paytable.</p>
	<p><strong>MATCH</strong> triggers a duel between two symbols, deciding a multiplier for the win.</p>
	<p><strong>SUPER LIKE</strong> sends out extra Wilds carrying its own multiplier.</p>
	<p><strong>DATE</strong> is the scatter symbol. Land 3 or 4 to unlock SPEED DATING or AFTER DARK.</p>

	<h2>WAYS TO WIN</h2>
	<p>You win when matching symbols land on adjacent reels, starting from the leftmost reel, along one of 19 fixed paylines. Only the highest win per line is paid.</p>

	<h2>BUY BONUS</h2>
	<p>Louvo lets you jump straight into the action from the BONUS button.</p>
	<p><strong>DATE X5</strong> \u2014 3x your bet \u2014 increases the chance of triggering a bonus round.</p>
	<p><strong>MATCH 2+</strong> \u2014 60x your bet \u2014 guarantees MATCH symbols on the next spin.</p>
	<p><strong>SUPER LIKE</strong> \u2014 60x your bet \u2014 guarantees a Super Like on the next spin.</p>
	<p><strong>SPEED DATING</strong> \u2014 80x your bet \u2014 instantly unlocks 10 free spins in the daytime setting.</p>
	<p><strong>AFTER DARK</strong> \u2014 150x your bet \u2014 instantly unlocks 10 free spins in the nighttime setting.</p>
</div>'''

old = """<Modals>
	{#snippet version()}
		<GameVersion version="0.0.0" />
	{/snippet}
</Modals>"""
new = f"""<Modals>
	{{#snippet version()}}
		<GameVersion version="0.0.0" />
	{{/snippet}}
	{{#snippet gameRules()}}
		{{@html `{RULES_HTML}`}}
	{{/snippet}}
</Modals>"""

if old not in content:
    print("ERREUR : ancre introuvable.")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : regles du jeu redigees et branchees sur la fenetre gameRules.")
