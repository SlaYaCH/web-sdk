path = "apps/louvo/src/components/SuperlikeHeartThrow.svelte"
with open(path, "r") as f:
    content = f.read()

old = """                                               reelSymbol.rawSymbol = { name: 'W', wild: true };
                                        }
                                        resolve();
                                        // Reste visible (pas de fondu) jusqu'au prochain spin,
                                        // comme la banniere qui l'accompagne.
                                }"""
new = """                                               reelSymbol.rawSymbol = { name: 'W', wild: true };
                                        }
                                        // Le coeur disparait immediatement : le vrai symbole WILD
                                        // prend le relais visuellement a cet instant precis.
                                        hearts[index].alpha = 0;
                                        resolve();
                                }"""

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : le coeur disparait exactement quand le wild se revele.")
