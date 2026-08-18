path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old = "\t\t<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>\n" \
      "\t\t\t<Text\n" \
      "\t\t\t\tanchor={{ x: 1, y: 0 }}\n" \
      "\t\t\t\ttext=\"ADD YOUR LOGO\"\n" \
      "\t\t\t\tstyle={{\n" \
      "\t\t\t\t\tfontFamily: 'proxima-nova',\n" \
      "\t\t\t\t\tfontSize: REM * 1.5,\n" \
      "\t\t\t\t\tfontWeight: '600',\n" \
      "\t\t\t\t\tlineHeight: REM * 2,\n" \
      "\t\t\t\t\tfill: 0xffffff,\n" \
      "\t\t\t\t}}\n" \
      "\t\t\t/>\n" \
      "\t\t</Container>"

new = "\t\t<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>\n" \
      "\t\t\t<Sprite key=\"louvoLogo\" anchor={{ x: 1, y: 0 }} width={100} height={72.8} />\n" \
      "\t\t</Container>"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : texte remplace par le vrai logo (badge ~100x73px, coin haut droit).")
