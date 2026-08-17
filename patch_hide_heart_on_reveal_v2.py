path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = """						}
					}
					resolve();
					// Reste visible (pas de fondu) jusqu'au prochain spin,
					// comme la banniere qui l'accompagne.
				}"""

new = """						}
					}
					// Le coeur disparait immediatement : le vrai symbole WILD
					// prend le relais visuellement a cet instant precis.
					hearts[index].alpha = 0;
					resolve();
				}"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1) - tentative avec des espaces plutot que des tabulations...")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : le coeur disparait exactement quand le wild se revele.")

# Si la version tabulation n'a pas marche, tenter avec la structure exacte
# telle que collee (au cas ou le fichier utilise des espaces)
if count != 1:
    import re
    pattern = re.compile(
        r"(\}\s*\n\s*resolve\(\);\s*\n\s*// Reste visible.*?\n\s*// comme la banniere.*?\n)(\s*\}\s*\n\s*\};)",
        re.DOTALL,
    )
    def repl(m):
        return (
            "}\n\t\t\t\t\t// Le coeur disparait immediatement : le vrai symbole WILD\n"
            "\t\t\t\t\t// prend le relais visuellement a cet instant precis.\n"
            "\t\t\t\t\thearts[index].alpha = 0;\n"
            "\t\t\t\t\tresolve();\n"
        ) + m.group(2)
    new_content, n = pattern.subn(repl, content)
    if n == 1:
        with open(path, "w") as f:
            f.write(new_content)
        print("OK (methode alternative) : le coeur disparait exactement quand le wild se revele.")
    else:
        print(f"ERREUR finale : {n} correspondance(s) trouvee(s) avec la methode alternative (attendu 1).")
