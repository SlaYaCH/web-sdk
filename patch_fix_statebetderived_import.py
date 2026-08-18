path = "apps/louvo/src/game/bookEventHandlerMap.ts"
with open(path, "r") as f:
    content = f.read()

old = "import { stateBet, stateUi } from 'state-shared';"
new = "import { stateBet, stateBetDerived, stateUi } from 'state-shared';"

count = content.count(old)
if count != 1:
    print(f"ERREUR : trouve {count} fois (attendu 1).")
else:
    content = content.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : stateBetDerived importe depuis state-shared, comme stateBet.")
