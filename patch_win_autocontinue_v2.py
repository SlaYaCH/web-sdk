path = "apps/louvo/src/components/Win.svelte"
with open(path, "r") as f:
    content = f.read()

old = "\t\t\t\t\tonmount={async () => {\n" \
      "\t\t\t\t\t\tawait startCountUp();\n" \
      "\t\t\t\t\t\tawait waitForTimeout(300);\n" \
      "\t\t\t\t\t\t// Reste affiche jusqu'au prochain spin (ou un clic manuel via\n" \
      "\t\t\t\t\t\t// PressToContinue) - plus de fermeture automatique ici.\n" \
      "\t\t\t\t\t}}"

new = "\t\t\t\t\tonmount={async () => {\n" \
      "\t\t\t\t\t\tawait startCountUp();\n" \
      "\t\t\t\t\t\tawait waitForTimeout(300);\n" \
      "\t\t\t\t\t\tif (!stateBet.stopOnWin) {\n" \
      "\t\t\t\t\t\t\tawait waitForTimeout(duration);\n" \
      "\t\t\t\t\t\t\toncomplete();\n" \
      "\t\t\t\t\t\t}\n" \
      "\t\t\t\t\t\t// Si stopOnWin est actif, reste affiche jusqu'a un clic manuel\n" \
      "\t\t\t\t\t\t// (PressToContinue) ou le prochain spin.\n" \
      "\t\t\t\t\t}}"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : auto-continue apres presentDuration, sauf si stopOnWin actif.")
