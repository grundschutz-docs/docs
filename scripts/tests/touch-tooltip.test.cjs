// Touch-Tooltip der Pillen (ControlMeta.astro): der Zusatz "Nochmal tippen: alle
// Anforderungen zu diesem Thema." darf nur an Themen-Pillen stehen, nicht an
// "Gilt für: <Zielobjekt>" und "Dokumentiert in: <Dokument>".
//
// Aufruf gegen einen fertigen Build (dist/):
//   NODE_PATH=<ordner mit playwright>/node_modules node scripts/tests/touch-tooltip.test.cjs [dist]
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const dist = path.resolve(process.argv[2] ?? 'dist');
const PAGE = '/grundschutzpp/konf/';

function serve() {
	const server = http.createServer((req, res) => {
		let file = path.join(dist, decodeURIComponent(new URL(req.url, 'http://x').pathname));
		if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
		if (!fs.existsSync(file)) {
			res.writeHead(404).end();
			return;
		}
		res.writeHead(200).end(fs.readFileSync(file));
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
		const context = await browser.newContext({ hasTouch: true, isMobile: true, viewport: { width: 390, height: 844 } });
		const page = await context.newPage();
		await page.goto(`http://localhost:${server.address().port}${PAGE}`);
		await page.waitForLoadState('networkidle');

		const touch = await page.evaluate(() => matchMedia('(hover: none)').matches);
		check(touch, 'Touch-Emulation aktiv ((hover: none) trifft zu), sonst beweist der Test nichts');

		const tooltips = await page.evaluate(() => {
			const pick = (sel) => [...document.querySelectorAll(sel)].map((a) => a.dataset.tooltip);
			return {
				themen: pick('a.pill[data-tooltip][href^="/grundschutzpp/themen/"]'),
				zielobjekte: pick('a.pill[data-tooltip][href^="/zielobjekte/"]'),
				dokumente: pick('a.pill[data-tooltip][href^="/dokumente/"]'),
			};
		});
		const SUFFIX = 'Nochmal tippen';
		check(tooltips.themen.length > 0, `Themen-Pillen vorhanden (${tooltips.themen.length})`);
		check(tooltips.zielobjekte.length > 0, `Zielobjekt-Pillen vorhanden (${tooltips.zielobjekte.length})`);
		check(tooltips.dokumente.length > 0, `Dokument-Pillen vorhanden (${tooltips.dokumente.length})`);
		check(
			tooltips.themen.length > 0 && tooltips.themen.every((t) => t.includes(SUFFIX)),
			'Themen-Pillen tragen den Zusatz (das Skript lief)',
		);
		check(
			!tooltips.zielobjekte.some((t) => t.includes(SUFFIX)),
			'Zielobjekt-Pillen tragen den Themen-Zusatz nicht',
		);
		check(!tooltips.dokumente.some((t) => t.includes(SUFFIX)), 'Dokument-Pillen tragen den Themen-Zusatz nicht');
	} finally {
		await browser.close();
		server.close();
	}
	process.exit(failed ? 1 : 0);
})();
