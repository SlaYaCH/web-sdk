path = "apps/louvo/src/components/Game.svelte"
with open(path, "r") as f:
    content = f.read()

marker = '<div class="louvo-rules">'
count = content.count(marker)
if count != 1:
    print(f"ERREUR : '{marker}' trouve {count} fois (attendu 1).")
else:
    style_block = """<style>
	.louvo-rules { color: #ffffff; line-height: 1.5; }
	.louvo-rules h2 { color: #ff2d6a; margin-top: 24px; }
	.louvo-rules h3 { color: #ff8fb3; margin-top: 16px; }
	.louvo-paytable-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
		gap: 12px;
		margin: 12px 0;
	}
	.louvo-paytable-item {
		text-align: center;
		font-size: 12px;
	}
	.louvo-paytable-item img {
		width: 56px;
		height: 56px;
		object-fit: contain;
		border-radius: 6px;
		display: block;
		margin: 0 auto 4px auto;
	}
	.louvo-paytable-item span {
		display: block;
	}
</style>
"""
    idx = content.index(marker)
    content = content[:idx] + style_block + content[idx:]
    with open(path, "w") as f:
        f.write(content)
    print("OK : CSS ajoute, images du paytable ramenees a 56x56px.")
