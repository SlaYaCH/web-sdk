path = "apps/louvo/src/components/Win.svelte"
with open(path, "r") as f:
    content = f.read()

old = (
    "\t\t\t\t\tonmount={async () => {\n"
    "\t\t\t\t\t\tawait startCountUp();\n"
    "\t\t\t\t\t\tawait waitForTimeout(300);\n"
    "\t\t\t\t\t\tif (!stateBet.stopOnWin) {\n"
    "\t\t\t\t\t\t\tawait waitForTimeout(duration);\n"
    "\t\t\t\t\t\t\toncomplete();\n"
    "\t\t\t\t\t\t}\n"
    "\t\t\t\t\t\t// Si stopOnWin est actif, reste affiche jusqu'a un clic manuel\n"
    "\t\t\t\t\t\t// (PressToContinue) ou le prochain spin.\n"
    "\t\t\t\t\t}}"
)

new = (
    "\t\t\t\t\tonmount={async () => {\n"
    "\t\t\t\t\t\tif (isBigWin) {\n"
    "\t\t\t\t\t\t\t// A partir de BIG WIN : compte depuis zero, reste affiche\n"
    "\t\t\t\t\t\t\t// le temps prevu pour la mise en scene.\n"
    "\t\t\t\t\t\t\tawait startCountUp();\n"
    "\t\t\t\t\t\t\tawait waitForTimeout(300);\n"
    "\t\t\t\t\t\t\tif (!stateBet.stopOnWin) {\n"
    "\t\t\t\t\t\t\t\tawait waitForTimeout(duration);\n"
    "\t\t\t\t\t\t\t\toncomplete();\n"
    "\t\t\t\t\t\t\t}\n"
    "\t\t\t\t\t\t} else {\n"
    "\t\t\t\t\t\t\t// En dessous de BIG WIN : affichage instantane, pas de\n"
    "\t\t\t\t\t\t\t// comptage depuis zero, enchainement direct sur le tour\n"
    "\t\t\t\t\t\t\t// suivant, sans aucune attente.\n"
    "\t\t\t\t\t\t\tfinishCountUp();\n"
    "\t\t\t\t\t\t\tif (!stateBet.stopOnWin) {\n"
    "\t\t\t\t\t\t\t\toncomplete();\n"
    "\t\t\t\t\t\t\t}\n"
    "\t\t\t\t\t\t}\n"
    "\t\t\t\t\t\t// Si stopOnWin est actif, reste affiche jusqu'a un clic manuel\n"
    "\t\t\t\t\t\t// (PressToContinue) ou le prochain spin, quel que soit le palier.\n"
    "\t\t\t\t\t}}"
)

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : gains en dessous de BIG WIN affiches instantanement et enchainent direct, big win+ garde le comptage.")
