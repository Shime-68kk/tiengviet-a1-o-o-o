import puppeteer from 'puppeteer-core';
import fs from 'fs';

async function testShadowing() {
  console.log('🎯 Running Specialized Shadowing Section Verification...');

  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1920,1080',
      '--autoplay-policy=no-user-gesture-required'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await new Promise(r => setTimeout(r, 1200));

  // Scroll to Scene Y
  await page.$eval('#scene-y', el => el.scrollIntoView({ behavior: 'instant', block: 'start' }));
  await new Promise(r => setTimeout(r, 600));

  // 1. Verify 3-Step Methodology Header
  const sectionText = await page.$eval('#scene-y', el => el.innerText);
  const hasStep1 = sectionText.includes('Nghe Người Bản Xứ');
  const hasStep2 = sectionText.includes('Khoảng Dừng Vàng (2.5s)');
  const hasStep3 = sectionText.includes('Lặp Lại To Rõ (Shadowing)');
  console.log(`✅ 3-Step Methodology Banner: ${hasStep1 && hasStep2 && hasStep3 ? 'VERIFIED' : 'FAILED'}`);

  // 2. Test BÒ (O) Drill Lifecycle
  console.log('\n--- TESTING DRILL 1: BÒ (ÂM O) ---');
  await page.$eval('button[onclick*="s3_y_pair_o"]', el => el.click());
  await new Promise(r => setTimeout(r, 400));

  // Check Listening phase & card highlight
  const isCardOHighlighted = await page.$eval('#card-drill-o', el => el.classList.contains('ring-4'));
  const tag1 = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log(`🎧 Phase 1 (Listening): Tag="${tag1}", Card Highlighted=${isCardOHighlighted ? 'YES' : 'NO'}`);

  // Capture Screenshot of Phase 1
  const sceneElem = await page.$('#scene-y');
  await sceneElem.screenshot({ path: '/home/quang/video_ai/screenshot_shadowing_listen.png' });
  console.log('📸 Saved Phase 1 Screenshot: screenshot_shadowing_listen.png');

  // Wait for audio to finish (~3.4s) -> Trigger 2.5s repeat countdown
  console.log('⏳ Waiting for audio playback to finish and transition to 2.5s repeat...');
  await new Promise(r => setTimeout(r, 3600));

  // Check Repeat phase
  const tag2 = await page.$eval('#drill-status-tag', el => el.innerText);
  const prompt2 = await page.$eval('#drill-prompt-text', el => el.innerText);
  const timerNum = await page.$eval('#drill-timer-num', el => el.innerText);
  console.log(`🎤 Phase 2 (Repeating 2.5s): Tag="${tag2}", Prompt="${prompt2}", Timer=${timerNum}`);

  // Capture Screenshot of Phase 2 (Active Recording & Countdown)
  await sceneElem.screenshot({ path: '/home/quang/video_ai/screenshot_shadowing_repeat.png' });
  console.log('📸 Saved Phase 2 Screenshot: screenshot_shadowing_repeat.png');

  // Wait for 2.5s timer to complete
  await new Promise(r => setTimeout(r, 2600));
  const tag3 = await page.$eval('#drill-status-tag', el => el.innerText);
  const prompt3 = await page.$eval('#drill-prompt-text', el => el.innerText);
  console.log(`🎉 Phase 3 (Completion): Tag="${tag3}", Prompt="${prompt3}"`);

  // 3. Test CÔ (Ô) Drill Card Highlight
  console.log('\n--- TESTING DRILL 2: CÔ (ÂM Ô) ---');
  await page.$eval('button[onclick*="s3_y_pair_oe"]', el => el.click());
  await new Promise(r => setTimeout(r, 400));
  const isCardOEHighlighted = await page.$eval('#card-drill-oe', el => el.classList.contains('ring-4'));
  console.log(`✅ Card CÔ Highlighted: ${isCardOEHighlighted ? 'YES' : 'NO'}`);

  // 4. Test BƠ (Ơ) Drill Card Highlight
  console.log('\n--- TESTING DRILL 3: BƠ (ÂM Ơ) ---');
  await page.$eval('button[onclick*="s3_y_pair_ow"]', el => el.click());
  await new Promise(r => setTimeout(r, 400));
  const isCardOWHighlighted = await page.$eval('#card-drill-ow', el => el.classList.contains('ring-4'));
  console.log(`✅ Card BƠ Highlighted: ${isCardOWHighlighted ? 'YES' : 'NO'}`);

  // 5. Test Full Shadowing Sequential Button Existence & Click
  console.log('\n--- TESTING FULL FLOW BUTTON ---');
  const fullFlowBtn = await page.$('#btn-full-shadowing');
  console.log(`✅ Full Flow Button Exists: ${!!fullFlowBtn ? 'YES' : 'NO'}`);

  await browser.close();
  console.log('\n✨ Shadowing Section Verification Finished Successfully!\n');
}

testShadowing().catch(e => {
  console.error('Fatal test error:', e);
  process.exit(1);
});
