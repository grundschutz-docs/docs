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
			// Der Hinweis steht als Kind-Element .pill-tip in der Pille (nicht mehr im Attribut data-tooltip).
			const pick = (sel) => [...document.querySelectorAll(sel)].map((a) => a.textContent);
			return {
				themen: pick('a.pill[href^="/grundschutzpp/themen/"] > .pill-tip'),
				zielobjekte: pick('a.pill[href^="/zielobjekte/"] > .pill-tip'),
				dokumente: pick('a.pill[href^="/dokumente/"] > .pill-tip'),
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

		// Pillen ohne Link sind nicht fokussierbar; ein Tipp schaltet den Hinweis um.
		const pill = page.locator('span.pill:has(> .pill-tip)').first();
		const sichtbar = () => pill.locator('> .pill-tip').evaluate((el) => Number(getComputedStyle(el).opacity) > 0.5);
		check(!(await sichtbar()), 'Hinweis ist vor dem Tippen unsichtbar');
		await pill.tap();
		await page.waitForTimeout(300);
		check(await sichtbar(), 'Tippen auf eine Pille ohne Link zeigt den Hinweis');
		await page.mouse.click(5, 300);
		await page.waitForTimeout(300);
		check(!(await sichtbar()), 'Tippen daneben schliesst den Hinweis');
		const tabstops = await page.evaluate(() => document.querySelectorAll('span.pill[tabindex]').length);
		check(tabstops === 0, `Pillen ohne Link sind keine Tab-Stops (${tabstops})`);
	} finally {
		await browser.close();
		server.close();
	}
	process.exit(failed ? 1 : 0);
})();
