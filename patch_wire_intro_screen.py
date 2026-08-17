path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

old_import = "import LoadingScreen from './LoadingScreen.svelte';"
new_import = old_import + "\nimport LouvoIntroScreen from './LouvoIntroScreen.svelte';"

old_state = "\tlet bonusMenuOpen = $state(false);"
new_state = "\tlet bonusMenuOpen = $state(false);\n\tlet showIntroScreen = $state(false);"

old_block = """{#if context.stateLayout.showLoadingScreen}
\t\t<LoadingScreen onloaded={() => (context.stateLayout.showLoadingScreen = false)} />
\t{:else}"""
new_block = """{#if context.stateLayout.showLoadingScreen}
\t\t<LoadingScreen
\t\t\tonloaded={() => {
\t\t\t\tcontext.stateLayout.showLoadingScreen = false;
\t\t\t\tshowIntroScreen = true;
\t\t\t}}
\t\t/>
\t{:else if showIntroScreen}
\t\t<LouvoIntroScreen onpress={() => (showIntroScreen = false)} />
\t{:else}"""

missing = [n for n, o in [("import", old_import), ("state", old_state), ("block", old_block)] if o not in content]
if missing:
    print("ERREUR Game.svelte : ancre(s) introuvable(s) :", missing)
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_state, new_state, 1)
    content = content.replace(old_block, new_block, 1)
    with open(path, "w") as f:
        f.write(content)
    print("OK : ecran d'accueil branche entre chargement et jeu.")
