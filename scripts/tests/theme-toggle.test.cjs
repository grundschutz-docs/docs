// ThemeToggle (ThemeToggle.astro): Starlight bindet ihn zweimal ein (Kopfzeile und Menue fuer
// schmale Bildschirme). Ein Klick muss beide Instanzen aktualisieren, sonst zeigt die zweite beim
// Oeffnen des Menues ein altes Symbol und eine falsche Beschriftung.
//
// Aufruf gegen einen fertigen Build:
//   NODE_PATH=<ordner mit playwright>/node_modules node scripts/tests/theme-toggle.test.cjs [dist]
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const dist = path.resolve(process.argv[2] ?? 'dist');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.json': 'application/json', '.woff2': 'font/woff2' };

function serve() {
	const server = http.createServer((req, res) => {
		let file = path.join(dist, decodeURIComponent(new URL(req.url, 'http://x').pathname));
		if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
		if (!fs.existsSync(file)) return void res.writeHead(404).end();
		res.writeHead(200, { 'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream' }).end(fs.readFileSync(file));
	});
	return new Promise((resolve) => server.listen(0, () => resolve(server)));
}

(async () => {
	const server = await serve();
	const browser = await chromium.launch();
	let failed = false;
	const check = (ok, msg) => {
		console.log(`${ok ? 'ok     ' : 'FEHLER '}${msg}`);
		if (!ok) failed = true;
	};
	try {
		const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, colorScheme: 'light' });
		const page = await context.newPage();
		// Eine Seite mit Sidebar: nur dort gibt es das Menue fuer schmale Bildschirme mit der zweiten Instanz.
		await page.goto(`http://localhost:${server.address().port}/methodik/`);
		await page.waitForLoadState('networkidle');
		const zustand = () =>
			page.evaluate(() =>
				[...document.querySelectorAll('theme-toggle')].map((t) => ({
					active: t.dataset.active,
					label: t.querySelector('button')?.getAttribute('aria-label'),
					sichtbar: t.getClientRects().length > 0,
				})),
			);
		const vorher = await zustand();
		check(vorher.length >= 2, `mindestens zwei Instanzen auf der Seite (${vorher.length})`);
		await page.locator('theme-toggle button:visible').first().click();
		const nachher = await zustand();
		check(nachher.every((t) => t.active === nachher[0].active), `alle Instanzen zeigen dieselbe Stufe nach dem Klick: ${JSON.stringify(nachher.map((t) => t.active))}`);
		check(nachher.every((t) => t.label === nachher[0].label && t.label), `alle Instanzen haben dieselbe Beschriftung: ${JSON.stringify(nachher.map((t) => t.label))}`);
		const seitenTheme = await page.evaluate(() => document.documentElement.dataset.theme);
		check(seitenTheme === nachher[0].active, `die Seite selbst hat das Theme gewechselt (data-theme=${seitenTheme})`);
		check(nachher[0].active !== vorher[0].active, 'der Klick hat die Stufe wirklich gewechselt (sonst beweist der Test nichts)');
	} finally {
		await browser.close();
		server.close();
	}
	process.exit(failed ? 1 : 0);
})();
