// Druck (@media print): Bedienelemente ohne Sinn auf Papier duerfen nicht mitgedruckt werden.
// Auf /export/ waren das das Formular und der klebende (position: sticky) Ergebnisbalken mit
// sieben Knoepfen, auf /vergleich/ das Suchfeld.
//
// Aufruf gegen einen fertigen Build:
//   NODE_PATH=<ordner mit playwright>/node_modules node scripts/tests/print.test.cjs [dist]
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const dist = path.resolve(process.argv[2] ?? 'dist');
const CASES = [
	['/export/', ['.export-form', '.export-result']],
	['/vergleich/', ['.vergleich-search']],
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
	let failed = false;
	const check = (ok, msg) => {
		console.log(`${ok ? 'ok     ' : 'FEHLER '}${msg}`);
		if (!ok) failed = true;
	};
	try {
		const page = await browser.newPage({ viewport: { width: 1100, height: 800 } });
		for (const [url, selectors] of CASES) {
			await page.goto(`http://localhost:${server.address().port}${url}`);
			await page.waitForLoadState('networkidle');
			// Gegenprobe vor dem Druck: das Element gibt es und es ist auf dem Bildschirm sichtbar.
			for (const sel of selectors) {
				const onScreen = await page.evaluate((s) => {
					const e = document.querySelector(s);
					return !!e && getComputedStyle(e).display !== 'none';
				}, sel);
				check(onScreen, `${url} ${sel}: auf dem Bildschirm vorhanden`);
			}
			await page.emulateMedia({ media: 'print' });
			for (const sel of selectors) {
				const shown = await page.evaluate((s) => getComputedStyle(document.querySelector(s)).display !== 'none', sel);
				check(!shown, `${url} ${sel}: im Druck ausgeblendet`);
			}
			await page.emulateMedia({ media: 'screen' });
		}
	} finally {
		await browser.close();
		server.close();
	}
	process.exit(failed ? 1 : 0);
})();
