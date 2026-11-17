// Renders design/banner.html to .github/images/banner-{dark,light}.png (1280x640, @2x).
// Needs Playwright (see ci.yml): node design/render-banner.cjs [outDir]
const path = require('path');
const { webkit } = require(require.resolve('@playwright/test', { paths: [process.env.PW_DIR || __dirname] }));
(async () => {
  const out = process.argv[2] || path.join(__dirname, '..', '.github', 'images');
  const browser = await webkit.launch();
  const V = process.env.V || 'a';
  for (const [name, qs] of [['dark', `?v=${V}`], ['light', `?v=${V}&day=1`]]) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 640 }, deviceScaleFactor: 2 });
    await page.goto('file://' + path.join(__dirname, 'banner.html') + qs);
    await page.locator('#banner').screenshot({ path: path.join(out, `banner-${V}-${name}.png`) });
  }
  await browser.close();
})();
