path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

marker = "\t.louvo-rules { color: #ffffff; line-height: 1.5; }"
count = content.count(marker)
if count != 1:
    print(f"ERREUR : marqueur trouve {count} fois (attendu 1).")
else:
    new_line = (
        "\t.louvo-rules {\n"
        "\t\tcolor: #ffffff;\n"
        "\t\tline-height: 1.5;\n"
        "\t\tmax-height: 80vh;\n"
        "\t\toverflow-y: auto;\n"
        "\t\tpadding-right: 12px;\n"
        "\t\tbox-sizing: border-box;\n"
        "\t}"
    )
    content = content.replace(marker, new_line, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : le contenu des regles a maintenant sa propre zone de defilement bornee (80% de la hauteur d'ecran).")
