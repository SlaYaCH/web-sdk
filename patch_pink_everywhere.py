paths = [
    "apps/louvo/src/components/Win.svelte",
    "apps/louvo/src/components/GlobalMultiplier.svelte",
    "apps/louvo/src/components/FreeSpinIntro.svelte",
    "apps/louvo/src/components/FreeSpinCounter.svelte",
    "apps/louvo/src/components/BannerReveal.svelte",
    "apps/louvo/src/components/Symbol.svelte",
]

old = "fontFamily: 'gold',"
new = "fontFamily: 'gold', fill: 0xff2d6a,"

for path in paths:
    with open(path, "r") as f:
        content = f.read()
    count = content.count(old)
    if count == 0:
        print(f"ERREUR {path} : aucune occurrence trouvee.")
        continue
    content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)
    print(f"OK : {path} - {count} occurrence(s) recoloree(s).")
