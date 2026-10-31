// Zugaenglichkeit: axe-core gegen einen fertigen Build, helles und dunkles Theme, Desktop- und Handy-Breite.
//
// Geprueft werden die WCAG-Regeln 2.0/2.1 A und AA (dazu gehoert der Farbkontrast, den
// CONTRIBUTING.md verlangt). Die "best-practice"-Regeln fehlen mit Absicht: sie melden
// Starlight-eigenes Markup (Skip-Link, doppelte Landmark im rechten Seitenrand).
//
// Aufruf:
//   NODE_PATH=<ordner mit playwright und axe-core>/node_modules node scripts/tests/a11y.test.cjs [dist]
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const dist = path.resolve(process.argv[2] ?? 'dist');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// Je ein Vertreter jedes Seitentyps, dazu alle Seiten mit eigenem Bauteil.
const PAGES = [
	'/', '/en/', '/export/', '/methodik/', '/en/methodik/', '/rag/', '/ueber/', '/aenderungen/',
	'/rollen/geschaeftsfuehrung/', '/rollen/isb/', '/rollen/devs/',
	'/grundschutzpp/zeitplan/', '/grundschutzpp/stm/', '/grundschutzpp/gc/', '/grundschutzpp/konf/', '/grundschutzpp/themen/',
	'/zielobjekte/', '/zielobjekte/webserver/', '/dokumente/', '/dokumente/detektions-konzept/',
	'/vergleich/', '/vergleich/sys-1-1/', '/vergleich/isms-1/', '/befunde/', '/befunde/mapping-datei-ist-entwurf/',
	'/en/operating-in-germany/', '/impressum/', '/404.html',
];
const VARIANTS = [
	['light', { width: 1280, height: 900 }],
	['dark', { width: 1280, height: 900 }],
	['light', { width: 390, height: 844 }],
	['dark', { width: 390, height: 844 }],
];
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
	const problems = [];
	let checked = 0;
	try {
		// Desktop und Handy-Breite: auf dem Handy laufen Tabellen ueber und werden scrollbar.
		for (const [theme, viewport] of VARIANTS) {
			const context = await browser.newContext({ viewport, colorScheme: theme });
			const page = await context.newPage();
			for (const url of PAGES) {
				const res = await page.goto(`http://localhost:${server.address().port}${url}`);
				if (!res || (res.status() !== 200 && url !== '/404.html')) {
					problems.push(`${theme}/${viewport.width} ${url}: Seite nicht erreichbar (${res?.status()})`);
					continue;
				}
				await page.waitForLoadState('networkidle');
				await page.evaluate(axeSource);
				const result = await page.evaluate(() =>
					axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } }),
				);
				checked += 1;
				for (const v of result.violations) {
					problems.push(`${theme}/${viewport.width} ${url}: ${v.id} [${v.impact}] x${v.nodes.length}, z. B. ${v.nodes[0].target.join(' ')}`);
				}
			}
			await context.close();
		}
	} finally {
		await browser.close();
		server.close();
	}
	console.log(`${checked} Seitenpruefungen (${PAGES.length} Seiten x ${VARIANTS.length} Varianten)`);
	for (const p of problems) console.log(`FEHLER ${p}`);
	if (!problems.length) console.log('ok     keine WCAG-Verstoesse');
	process.exit(problems.length || checked !== PAGES.length * VARIANTS.length ? 1 : 0);
})();
