// Rechte Leiste "Auf dieser Seite" (.right-sidebar): Starlight gibt ihr position: fixed und width: 100%,
// das bezieht sich auf das Fenster. Ohne die Breite in custom.css war die Glas-Kachel so breit wie das
// Fenster (1440 px in einer Spalte von 360 px) und ihr rechter Rand lag ausserhalb: kein Rand, keine
// Rundung, kein Schatten. Der Test prueft bei mehreren Fensterbreiten, dass die Kachel in ihrer Spalte
// liegt, im Fenster endet und rechts denselben Abstand hat wie die linke Leiste am linken Rand.
//
// Aufruf gegen einen fertigen Build:
//   NODE_PATH=<ordner mit playwright>/node_modules node scripts/tests/layout-rechte-leiste.test.cjs [dist]
// Lokal, wenn die Chromium-Version nicht zu Playwright passt: CHROMIUM_PATH=<Programm> davor setzen.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const dist = path.resolve(process.argv[2] ?? 'dist');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.json': 'application/json', '.woff2': 'font/woff2' };
// Ab 72rem (1152 px) gibt es die Spalte; 2560 px prueft, dass die Formel auch bei viel Platz stimmt.
const BREITEN = [1152, 1280, 1440, 1920, 2560];
const SEITEN = ['/methodik/', '/grundschutzpp/', '/en/methodik/'];
const TOLERANZ = 1.5; // Pixel (Rundung)

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
	const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
	let failed = false;
	const check = (ok, msg) => {
		console.log(`${ok ? 'ok     ' : 'FEHLER '}${msg}`);
		if (!ok) failed = true;
	};
	try {
		for (const breite of BREITEN) {
			const context = await browser.newContext({ viewport: { width: breite, height: 900 } });
			await context.route(/analytics\.kryptomrx\.de/, (r) => r.abort());
			const page = await context.newPage();
			for (const seite of SEITEN) {
				await page.goto(`http://localhost:${server.address().port}${seite}`, { waitUntil: 'load' });
				const g = await page.evaluate(() => {
					const rect = (s) => {
						const e = document.querySelector(s);
						if (!e) return null;
						const b = e.getBoundingClientRect();
						return { l: b.left, r: b.right, w: b.width };
					};
					return {
						fenster: document.documentElement.clientWidth,
						links: rect('.sidebar-pane'),
						spalte: rect('.right-sidebar-container'),
						leiste: rect('.right-sidebar'),
						scroll: document.documentElement.scrollWidth,
					};
				});
				const name = `${breite} px ${seite}`;
				if (!g.leiste || !g.spalte || !g.links) {
					check(false, `${name}: Leiste, Spalte oder linke Sidebar fehlt`);
					continue;
				}
				check(g.leiste.r <= g.fenster + TOLERANZ, `${name}: rechter Rand der Kachel liegt im Fenster (${Math.round(g.leiste.r)} von ${g.fenster})`);
				check(g.leiste.l >= g.spalte.l - TOLERANZ && g.leiste.r <= g.spalte.r + TOLERANZ, `${name}: Kachel liegt in ihrer Spalte (${Math.round(g.leiste.l)}-${Math.round(g.leiste.r)} in ${Math.round(g.spalte.l)}-${Math.round(g.spalte.r)})`);
				const rechts = g.fenster - g.leiste.r;
				check(Math.abs(rechts - g.links.l) <= TOLERANZ, `${name}: Abstand zum rechten Fensterrand (${rechts.toFixed(1)}) gleich dem der linken Leiste (${g.links.l.toFixed(1)})`);
				check(g.scroll <= g.fenster + TOLERANZ, `${name}: kein seitliches Scrollen der Seite (${g.scroll} bei ${g.fenster})`);
			}
			await context.close();
		}
	} finally {
		await browser.close();
		server.close();
	}
	if (failed) {
		console.error('\nDie rechte Leiste liegt nicht wie erwartet in ihrer Spalte.');
		process.exit(1);
	}
})();
