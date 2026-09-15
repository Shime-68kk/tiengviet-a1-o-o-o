import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 1200));

  // Hide sticky header & sticky footer during section screenshot for 100% clean view
  await page.evaluate(() => {
    document.getElementById('main-nav').style.display = 'none';
    document.getElementById('sticky-audio-bar').style.display = 'none';
  });

  const box = await page.$eval('#scene-y', el => {
    const r = el.getBoundingClientRect();
    return { x: r.left, y: window.scrollY + r.top, width: r.width, height: r.height };
  });

  // Capture clean idle/listening state
  await page.screenshot({
    path: '/home/quang/video_ai/screenshot_shadowing_clean.png',
    clip: { x: 0, y: Math.floor(box.y), width: 1920, height: Math.ceil(box.height) }
  });
  console.log('Saved clean screenshot');

  // Trigger BÒ drill
  await page.evaluate(() => triggerDrill('O', 'BÒ', 's3_y_pair_o'));
  await new Promise(r => setTimeout(r, 600));

  // Capture listening phase with active card
  await page.screenshot({
    path: '/home/quang/video_ai/screenshot_shadowing_active_listen.png',
    clip: { x: 0, y: Math.floor(box.y), width: 1920, height: Math.ceil(box.height) }
  });
  console.log('Saved active listen screenshot');

  // Wait 3.5s for teacher audio to finish and enter 2.5s repeat mode
  await new Promise(r => setTimeout(r, 3400));
  await page.screenshot({
    path: '/home/quang/video_ai/screenshot_shadowing_active_repeat.png',
    clip: { x: 0, y: Math.floor(box.y), width: 1920, height: Math.ceil(box.height) }
  });
  console.log('Saved active repeat screenshot');

  await browser.close();
})();
