path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

old = """import anticipationSpine from '../../assets/spines/anticipation';
import bigwinSpine from '../../assets/spines/bigwin';

export default {
	anticipation: { type: 'spine', ...anticipationSpine },
	bigwin: { type: 'spine', ...bigwinSpine },"""
new = "export default {"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : imports Spine casses retires, le build devrait remarcher.")
