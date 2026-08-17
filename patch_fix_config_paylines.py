import json

path = "apps/louvo/src/game/config.ts"
with open(path, "r") as f:
    content = f.read()

correct_paylines = {
    "1": [0,0,0,0,0], "2": [1,1,1,1,1], "3": [2,2,2,2,2], "4": [3,3,3,3,3], "5": [4,4,4,4,4],
    "6": [0,1,0,1,0], "7": [1,2,1,2,1], "8": [2,3,2,3,2], "9": [3,4,3,4,3], "10": [1,0,1,0,1],
    "11": [2,1,2,1,2], "12": [3,2,3,2,3], "13": [4,3,4,3,4], "14": [0,1,2,3,4], "15": [1,2,3,2,1],
    "16": [2,3,4,3,2], "17": [4,3,2,1,0], "18": [3,2,1,2,3], "19": [2,1,0,1,2],
}

# Localiser le bloc "paylines": { ... } et son etendue exacte (comptage d'accolades)
key = '"paylines"'
start = content.index(key)
brace_start = content.index('{', start)
depth = 0
end = brace_start
for i, c in enumerate(content[brace_start:], brace_start):
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break

old_block = content[brace_start:end]

# Verifier que l'ancien bloc correspond bien a ce qu'on attend (les valeurs buguees)
old_parsed = json.loads(old_block)
expected_old = {
    "1": [0,0,0,0,0], "2": [1,1,1,1,1], "3": [2,2,2,2,2], "4": [3,3,3,3,3], "5": [4,4,4,4,4],
    "6": [0,1,1,1,0], "7": [4,3,3,3,4], "8": [1,2,2,2,1], "9": [3,2,2,2,3], "10": [2,1,1,1,2],
    "11": [2,3,3,3,2], "12": [0,0,1,0,0], "13": [4,4,3,4,4], "14": [1,1,0,1,1], "15": [3,3,4,3,3],
    "16": [1,1,2,1,1], "17": [3,3,2,3,3], "18": [0,1,2,1,0], "19": [4,3,2,3,4],
}

if old_parsed != expected_old:
    print("ERREUR : le bloc paylines actuel ne correspond pas exactement a ce qui etait attendu - verification manuelle necessaire, rien modifie.")
else:
    # Reconstruire le bloc au meme format (indentation a la tabulation, comme le fichier .ts)
    lines = ['{']
    keys = sorted(correct_paylines, key=int)
    for idx, k in enumerate(keys):
        vals = correct_paylines[k]
        lines.append(f'\t\t"{k}": [')
        for v in vals:
            lines.append(f'\t\t\t{v},')
        # retirer la virgule finale du dernier element
        lines[-1] = lines[-1].rstrip(',')
        comma = ',' if idx < len(keys) - 1 else ''
        lines.append(f'\t\t]{comma}')
    lines.append('\t}')
    new_block = '\n'.join(lines)

    content = content[:brace_start] + new_block + content[end:]
    with open(path, "w") as f:
        f.write(content)
    print("OK : config.ts mis a jour avec les 19 vraies formes de lignes (alignees sur le Math SDK).")
