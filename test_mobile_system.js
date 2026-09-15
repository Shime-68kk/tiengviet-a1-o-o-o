import puppeteer from 'puppeteer-core';

async function testMobileSystem() {
  console.log('📱 Starting Dedicated Mobile System & UI Verification Test...');
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=390,844',
      '--autoplay-policy=no-user-gesture-required'
    ]
  });

  const page = await browser.newPage();
  // Set iPhone 14 Pro mobile viewport
  await page.setViewport({
    width: 390,
    height: 844,
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true
  });

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await new Promise(r => setTimeout(r, 1200));

  console.log('--- TEST 1: Check Technical Badges Removal ---');
  const pageContent = await page.content();
  const forbiddenPhrases = [
    'Sân khấu 3D Đứng Vững • Không Xoay Vòng',
    'Three.js WebGL',
    'Full Flow'
  ];
  for (const phrase of forbiddenPhrases) {
    if (pageContent.includes(phrase)) {
      throw new Error(`FAILED: Found forbidden technical phrase on page: "${phrase}"`);
    }
  }
  console.log('✅ TEST 1 PASSED: All technical dev notes completely removed!');

  console.log('--- TEST 2: Check Dedicated Mobile Learning Dock ---');
  const isMobileNavVisible = await page.$eval('#mobile-nav-dock', el => {
    const style = window.getComputedStyle(el);
    return style.display !== 'none' && style.visibility !== 'hidden';
  });
  console.log('Mobile floating nav dock visible on 390px viewport:', isMobileNavVisible);
  if (!isMobileNavVisible) throw new Error('FAILED: #mobile-nav-dock not visible on mobile viewport.');
  console.log('✅ TEST 2 PASSED: Dedicated Mobile Dock is active and visible.');

  console.log('--- TEST 3: Check 3D Canvas Mobile Attributes ---');
  const canvasTouchAction = await page.$eval('#three-canvas-container', el => window.getComputedStyle(el).touchAction);
  console.log('Canvas touch-action:', canvasTouchAction);
  if (canvasTouchAction !== 'pan-y') throw new Error(`FAILED: Canvas touchAction is not pan-y, got ${canvasTouchAction}`);
  console.log('✅ TEST 3 PASSED: 3D Canvas allows vertical scroll without hijacking.');

  console.log('--- TEST 4: Test Mobile Vowel Switcher Tabs in Section 3 ---');
  await page.$eval('#scene-y', el => el.scrollIntoView({ behavior: 'instant', block: 'start' }));
  await new Promise(r => setTimeout(r, 500));

  // Check mobile tabs visible
  const isMTabOVisible = await page.$eval('#m-tab-o', el => {
    const style = window.getComputedStyle(el);
    return style.display !== 'none';
  });
  console.log('Mobile vowel tab O visible:', isMTabOVisible);
  if (!isMTabOVisible) throw new Error('FAILED: Mobile vowel tab O is not visible.');

  // Click Mobile Tab CÔ (Ô)
  console.log('Clicking Mobile Tab Ô (CÔ)...');
  await page.click('#m-tab-oe');
  await new Promise(r => setTimeout(r, 400));

  // Verify drill status
  const drillStatus = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('Drill status after clicking mobile tab Ô:', drillStatus);
  if (!drillStatus.includes('Ô') && !drillStatus.includes('CÔ')) {
    throw new Error(`FAILED: Drill Ô was not triggered, got "${drillStatus}"`);
  }
  console.log('✅ TEST 4 PASSED: Mobile Vowel Tab switches seamlessly and starts drill!');

  // Capture screenshot of mobile view
  await page.screenshot({ path: '/home/quang/video_ai/screenshot_mobile_verified.png' });
  console.log('📸 Screenshot saved to screenshot_mobile_verified.png');

  if (consoleErrors.length > 0) {
    throw new Error(`FAILED with console errors: ${consoleErrors.join(', ')}`);
  }

  await browser.close();
  console.log('🎉 ALL MOBILE VERIFICATION TESTS PASSED WITH 0 ERRORS!');
}

testMobileSystem().catch(err => {
  console.error('❌ TEST FAILED:', err);
  process.exit(1);
});
