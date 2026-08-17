path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_paylines = """paylines = {
    1: [0,0,0,0,0], 2: [1,1,1,1,1], 3: [2,2,2,2,2], 4: [3,3,3,3,3], 5: [4,4,4,4,4],
    6: [0,1,1,1,0], 7: [4,3,3,3,4], 8: [1,2,2,2,1], 9: [3,2,2,2,3], 10: [2,1,1,1,2],
    11: [2,3,3,3,2], 12: [0,0,1,0,0], 13: [4,4,3,4,4], 14: [1,1,0,1,1], 15: [3,3,4,3,3],
    16: [1,1,2,1,1], 17: [3,3,2,3,3], 18: [0,1,2,1,0], 19: [4,3,2,3,4],
}"""

new_paylines = """paylines = {
    1: [0,0,0,0,0], 2: [1,1,1,1,1], 3: [2,2,2,2,2], 4: [3,3,3,3,3], 5: [4,4,4,4,4],
    6: [0,1,0,1,0], 7: [1,2,1,2,1], 8: [2,3,2,3,2], 9: [3,4,3,4,3], 10: [1,0,1,0,1],
    11: [2,1,2,1,2], 12: [3,2,3,2,3], 13: [4,3,4,3,4], 14: [0,1,2,3,4], 15: [1,2,3,2,1],
    16: [2,3,4,3,2], 17: [4,3,2,1,0], 18: [3,2,1,2,3], 19: [2,1,0,1,2],
}"""

if old_paylines not in content:
    print("ERREUR : ancre des paylignes introuvable.")
else:
    content = content.replace(old_paylines, new_paylines, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : les 19 diagrammes affichent maintenant exactement les formes de Duel at Dawn (apercu frontend, en attendant la vraie mise a jour Math SDK demain).")
