import puppeteer from 'puppeteer-core';

async function testStudio4() {
  console.log('🚀 Testing Studio Shadowing 4.0 & Dual Comparison Drawer...');
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1440,900',
      '--autoplay-policy=no-user-gesture-required'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  await page.goto('http://localhost:3000/#scene-y', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await new Promise(r => setTimeout(r, 1000));

  await page.$eval('#scene-y', el => el.scrollIntoView({ behavior: 'instant', block: 'start' }));
  await new Promise(r => setTimeout(r, 500));

  // Trigger Drill BÒ
  console.log('Triggering Drill BÒ...');
  await page.evaluate(() => {
    window.triggerDrill('O', 'BÒ', 's3_y_pair_o');
  });

  // Wait for countdown
  await page.waitForFunction(() => {
    const tag = document.getElementById('drill-status-tag');
    return tag && tag.innerText.includes('ĐẾN LƯỢT BẠN');
  }, { timeout: 10000 });

  // Wait for completion (2.5s)
  await page.waitForFunction(() => {
    const tag = document.getElementById('drill-status-tag');
    return tag && tag.innerText.includes('Hoàn thành');
  }, { timeout: 6000 });

  // Verify Comparison Station is now visible
  const isStationVisible = await page.$eval('#drill-comparison-station', el => !el.classList.contains('hidden'));
  console.log('Comparison Station visible:', isStationVisible);
  if (!isStationVisible) {
    throw new Error('FAILED: Comparison Station did not appear after drill completion.');
  }

  // Check Rubric Pills
  const pillsCount = await page.$$eval('.rubric-pill', els => els.length);
  console.log('Rubric criteria pills count:', pillsCount);
  if (pillsCount !== 2) {
    throw new Error('FAILED: Expected 2 rubric pills for vowel O, found: ' + pillsCount);
  }

  // Click each pill to test self-check
  const pills = await page.$$('.rubric-pill');
  for (const pill of pills) {
    await pill.click();
    await new Promise(r => setTimeout(r, 100));
  }

  // Check if completion badge appeared
  const badgeVisible = await page.$eval('#rubric-badge', el => !el.classList.contains('hidden'));
  console.log('Rubric achievement badge visible:', badgeVisible);
  if (!badgeVisible) {
    throw new Error('FAILED: Rubric achievement badge did not appear after checking all pills.');
  }

  // Test Dual-Voice buttons
  console.log('Testing Teacher Model playback...');
  await page.evaluate(() => window.playTeacherModelAudio());
  await new Promise(r => setTimeout(r, 500));

  console.log('Testing Sequential Comparison...');
  await page.evaluate(() => window.playSequentialComparison());
  await new Promise(r => setTimeout(r, 500));

  // Capture screenshot of Studio 4.0
  await page.screenshot({ path: 'screenshot_studio_4_verified.png' });
  console.log('📸 Screenshot saved to screenshot_studio_4_verified.png');

  await browser.close();
  console.log('🎉 STUDIO SHADOWING 4.0 TEST PASSED 100%!');
}

testStudio4().catch(err => {
  console.error('❌ Test error:', err);
  process.exit(1);
});
