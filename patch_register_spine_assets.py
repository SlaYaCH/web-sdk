path = "apps/louvo/src/game/assets.ts"
with open(path, "r") as f:
    content = f.read()

results = []

old_top = "export default {"
new_top = """import anticipationSpine from '../../assets/spines/anticipation';
import bigwinSpine from '../../assets/spines/bigwin';

export default {
	anticipation: { type: 'spine', ...anticipationSpine },
	bigwin: { type: 'spine', ...bigwinSpine },"""

count = content.count(old_top)
if count != 1:
    results.append(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old_top, new_top, 1)
    with open(path, "w") as f:
        f.write(content)
    results.append("OK : anticipation et bigwin importes et enregistres comme assets Spine.")

for r in results:
    print(r)
