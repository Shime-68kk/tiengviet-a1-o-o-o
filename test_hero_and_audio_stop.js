import puppeteer from 'puppeteer-core';

(async () => {
  console.log('🧪 Verifying Hero Layout and Audio Stop behavior...');
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 1200));

  // 1. Verify badge removal
  const bodyText = await page.$eval('body', el => el.innerText);
  const hasOldBadge = bodyText.includes('Dự Án Ngữ Âm Đạt Chuẩn 100/100 • 5 Thành Viên Nhóm');
  console.log(`Badge "Dự Án Ngữ Âm Đạt Chuẩn...": ${hasOldBadge ? 'STILL PRESENT ❌' : 'REMOVED COMPLETELY ✅'}`);

  // 2. Verify Hero title elements
  const h1Text = await page.$eval('#hero h1', el => el.innerText);
  console.log(`Hero H1 Text:\n"${h1Text}"`);

  // Capture Screenshot of Hero section
  const heroElem = await page.$('#hero');
  await heroElem.screenshot({ path: '/home/quang/video_ai/screenshot_hero_fixed.png' });
  console.log('📸 Saved Hero Section screenshot: screenshot_hero_fixed.png');

  // 3. Test Audio Non-Auto-Advance
  console.log('\n--- TESTING AUDIO NON-AUTO-ADVANCE ---');
  // Play short sound: s2_nhung_o_sound (~1.8s)
  await page.evaluate(() => playAudio('s2_nhung_o_sound'));
  const track1 = await page.$eval('#audio-track-title', el => el.innerText);
  console.log(`1. Started track: "${track1}"`);

  // Wait 3.0s (longer than the 1.8s track)
  console.log('⏳ Waiting for track to finish...');
  await new Promise(r => setTimeout(r, 3000));

  const trackAfterEnd = await page.$eval('#audio-track-title', el => el.innerText);
  const isPauseIconHidden = await page.$eval('#pause-icon', el => el.classList.contains('hidden'));
  const isPlayIconVisible = await page.$eval('#play-icon', el => !el.classList.contains('hidden'));

  console.log(`2. Track title after finish: "${trackAfterEnd}"`);
  console.log(`3. Player state stopped/paused: ${isPauseIconHidden && isPlayIconVisible ? 'YES (Stopped cleanly) ✅' : 'NO ❌'}`);
  const didNotAutoAdvance = trackAfterEnd.includes('Phát âm chuẩn: O');
  console.log(`4. Did not jump to next track: ${didNotAutoAdvance ? 'PASS ✅' : 'FAIL ❌'}`);

  await browser.close();

  if (!hasOldBadge && isPauseIconHidden && isPlayIconVisible && didNotAutoAdvance) {
    console.log('\n✨ ALL CHECKS PASSED PERFECTLY!');
    process.exit(0);
  } else {
    console.error('\n❌ SOME CHECKS FAILED!');
    process.exit(1);
  }
})();
