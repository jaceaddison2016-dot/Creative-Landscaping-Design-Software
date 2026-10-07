const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const fs = require('node:fs');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const L = require('../core.js');

(async () => {
  const options = { headless: true };
  if (process.env.BROWSER_EXECUTABLE) options.executablePath = process.env.BROWSER_EXECUTABLE;
  const browser = await chromium.launch(options);
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1080 },
    acceptDownloads: true,
  });
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  const output = path.resolve('test-results');
  fs.mkdirSync(output, { recursive: true });
  let server;
  try {
    server = spawn(process.execPath, ['scripts/serve.cjs'], {
      env: { ...process.env, PORT: '4181' },
    });
    await Promise.race([
      once(server.stdout, 'data'),
      once(server, 'error').then(([error]) => {
        throw error;
      }),
    ]);
    const initialURL = process.env.TEST_HTTP_ONLY
      ? 'http://127.0.0.1:4181'
      : pathToFileURL(path.resolve('index.html')).href;
    await page.goto(initialURL);
    await page.getByRole('button', { name: 'Shade tree' }).first().waitFor();
    assert.equal(await page.locator('#plan .plant').count(), 10);
    assert.equal(await page.locator('[data-layer="shadows"] polygon').count(), 10);
    await page.screenshot({ path: path.join(output, 'prototype.png'), fullPage: true });
    console.log(
      `PASS: ${process.env.TEST_HTTP_ONLY ? 'HTTP launch (file launch explicitly unrun)' : 'direct file launch'}, demo rendering, shadows`,
    );
    const clickPlan = async (x, y) => {
      const box = await page.locator('#plan').boundingBox();
      await page.mouse.click(box.x + x * box.width, box.y + y * box.height);
    };
    await page.getByRole('button', { name: 'New plan' }).click();
    assert.equal(await page.locator('#plan .plant').count(), 0);
    await page.locator('[data-kind="tree"]').click();
    await clickPlan(0.3, 0.3);
    assert.equal(await page.locator('#plan .plant').count(), 1);
    await page.locator('#select-tool').click();
    await page.locator('#plan .plant').click();
    await page.locator('#plant-name').fill('My maple');
    await page.locator('#plant-diameter').fill('12\' 6"');
    await page.locator('#plant-height').fill('20');
    await page.getByRole('button', { name: 'Apply changes' }).click();
    assert.match(await page.locator('#plan .plant').getAttribute('aria-label'), /My maple, 12′ 6″/);
    const before = await page.locator('#plan .plant circle').first().getAttribute('cx');
    const center = await page.locator('#plan .plant circle').first().boundingBox();
    await page.mouse.move(center.x + center.width / 2, center.y + center.height / 2);
    await page.mouse.down();
    await page.mouse.move(center.x + center.width / 2 + 55, center.y + center.height / 2 + 30, {
      steps: 6,
    });
    await page.mouse.up();
    assert.notEqual(await page.locator('#plan .plant circle').first().getAttribute('cx'), before);
    await page.locator('#undo').click();
    assert.equal(await page.locator('#plan .plant circle').first().getAttribute('cx'), before);
    await page.locator('#redo').click();
    assert.notEqual(await page.locator('#plan .plant circle').first().getAttribute('cx'), before);
    console.log('PASS: plant placement, imperial editing, drag, undo/redo');
    await page.locator('#measure-tool').click();
    await clickPlan(0.25, 0.7);
    await clickPlan(0.75, 0.7);
    assert.equal(await page.locator('#plan .dimension text').textContent(), '40′ 0″');
    await page.locator('#select-tool').click();
    await page.locator('#plan .dimension text').click();
    assert.equal(await page.locator('#dimension-value').textContent(), '40′ 0″');
    console.log('PASS: persistent 40-foot dimension and selection');
    const shadowBefore = await page
      .locator('[data-layer="shadows"] polygon')
      .getAttribute('points');
    await page.locator('#sun-date').fill('2026-12-21');
    await page.locator('#sun-time').fill('12:00');
    await page.getByRole('button', { name: 'Update sun study' }).click();
    assert.notEqual(
      await page.locator('[data-layer="shadows"] polygon').getAttribute('points'),
      shadowBefore,
    );
    await page.locator('#sun-time').fill('00:00');
    await page.getByRole('button', { name: 'Update sun study' }).click();
    assert.equal(await page.locator('[data-layer="shadows"] polygon').count(), 0);
    assert.equal(await page.locator('#sun-state').textContent(), 'SUN BELOW HORIZON');
    await page.locator('#sun-time').fill('12:00');
    await page.getByRole('button', { name: 'Update sun study' }).click();
    await page.locator('#show-shadows').uncheck();
    assert.equal(await page.locator('[data-layer="shadows"]').count(), 0);
    await page.locator('#show-shadows').check();
    console.log('PASS: seasonal shadows, midnight, visibility toggle');
    await page.locator('#project-name').fill('My first garden');
    await page.locator('#project-name').blur();
    const downloadEvent = page.waitForEvent('download');
    await page.locator('#save-project').click();
    const download = await downloadEvent;
    const saved = path.join(output, 'roundtrip.clp');
    await download.saveAs(saved);
    const project = L.parseProject(fs.readFileSync(saved, 'utf8'));
    assert.equal(project.name, 'My first garden');
    assert.equal(project.plants[0].height, 240);
    assert.equal(project.plants[0].diameter, 150);
    assert.equal(project.dimensions.length, 1);
    await page.locator('#new-project').click();
    assert.equal(await page.locator('#plan .plant').count(), 0);
    await page.locator('#file-input').setInputFiles(saved);
    await page.locator('#plan .plant').waitFor();
    assert.equal(await page.locator('#plan .plant').count(), 1);
    assert.equal(await page.locator('#plan .dimension').count(), 1);
    assert.equal(await page.locator('#project-name').inputValue(), 'My first garden');
    console.log('PASS: actual project download and reload preserves all features');
    const malformed = path.join(output, 'bad.clp');
    fs.writeFileSync(malformed, '{bad');
    await page.locator('#file-input').setInputFiles(malformed);
    await page.waitForFunction(() =>
      document.getElementById('status').textContent.includes('not valid JSON'),
    );
    assert.equal(await page.locator('#plan .plant').count(), 1);
    await page.locator('#plot-width').fill('10');
    await page.getByRole('button', { name: 'Update plot' }).click();
    assert.equal(await page.locator('#plan').getAttribute('viewBox'), '0 0 960 720');
    console.log('PASS: invalid files and out-of-bounds resizing preserve the existing plan');
    await page.locator('#select-tool').click();
    await page.locator('#plan .plant').click();
    await page.locator('#delete-selection').click();
    assert.equal(await page.locator('#plan .plant').count(), 0);
    await page.locator('#undo').click();
    assert.equal(await page.locator('#plan .plant').count(), 1);
    await page.locator('#project-name').fill('Unsaved plan');
    await page.locator('#project-name').blur();
    await page.locator('#new-project').click();
    await page.locator('#replace-dialog').waitFor();
    await page.getByRole('button', { name: 'Keep editing' }).click();
    assert.equal(await page.locator('#plan .plant').count(), 1);
    await page.locator('#new-project').click();
    await page.getByRole('button', { name: 'Replace plan' }).click();
    await page.waitForFunction(() => document.querySelectorAll('#plan .plant').length === 0);
    assert.equal(await page.locator('#plan .plant').count(), 0);
    console.log('PASS: delete/undo and unsaved replacement protection');
    // Untrusted plant labels must remain text, never HTML.
    const hostile = L.demoProject();
    hostile.plants[0].name = '<img src=x onerror=alert(1)>';
    const hostileFile = path.join(output, 'text.clp');
    fs.writeFileSync(hostileFile, L.serialize(hostile));
    await page.locator('#file-input').setInputFiles(hostileFile);
    await page.locator('#plan .plant').first().waitFor();
    await page.locator('#plan .plant').first().click();
    assert.equal(await page.locator('#plan img').count(), 0);
    assert.equal(await page.locator('#plant-name').inputValue(), hostile.plants[0].name);
    await page.setViewportSize({ width: 390, height: 844 });
    assert.ok(
      await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1),
    );
    console.log('PASS: text-safe labels and narrow screen layout');
    // Verify the optional development server serves the same working application.
    await page.goto('http://127.0.0.1:4181');
    await page.locator('#plan .plant').first().waitFor();
    assert.equal(await page.locator('#plan .plant').count(), 10);
    assert.deepEqual(errors, []);
    console.log('PASS: HTTP development startup; no browser runtime errors');
  } finally {
    if (server) server.kill();
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
