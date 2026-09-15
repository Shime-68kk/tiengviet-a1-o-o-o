import puppeteer from 'puppeteer-core';

async function runTests() {
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
  await page.setViewport({ width: 1440, height: 900 });

  console.log('🚀 Loading http://localhost:3000 with domcontentloaded...');
  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await new Promise(r => setTimeout(r, 1000));

  await page.$eval('#scene-y', el => el.scrollIntoView({ behavior: 'instant', block: 'start' }));
  await new Promise(r => setTimeout(r, 500));

  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('Browser console error:', msg.text());
    }
  });

  // TEST 1: Rapid clicking does not create orphaned intervals
  console.log('\n--- TEST 1: Rapid clicking BÒ -> CÔ -> BƠ ---');
  await page.evaluate(() => {
    window.triggerDrill('O', 'BÒ', 's3_y_pair_o');
    window.triggerDrill('Ô', 'CÔ', 's3_y_pair_oe');
    window.triggerDrill('Ơ', 'BƠ', 's3_y_pair_ow');
  });

  await new Promise(r => setTimeout(r, 400));
  const status1 = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('Status after rapid click:', status1);
  if (!status1.includes('Ơ — BƠ')) {
    throw new Error('TEST 1 FAILED: Latest drill (Ơ — BƠ) should be active, got: ' + status1);
  }
  console.log('✅ TEST 1 PASSED: Only the latest drill is active.');

  // TEST 2: Stop Drill button works cleanly
  console.log('\n--- TEST 2: Stop Drill Button ---');
  const stopBtnVisible = await page.$eval('#btn-stop-drill', el => window.getComputedStyle(el).display !== 'none');
  console.log('Stop button visible during drill:', stopBtnVisible);
  if (!stopBtnVisible) {
    throw new Error('TEST 2 FAILED: Stop button should be visible during active drill.');
  }

  await page.evaluate(() => document.getElementById('btn-stop-drill').click());
  await new Promise(r => setTimeout(r, 300));

  const timerNumAfterStop = await page.$eval('#drill-timer-num', el => el.innerText);
  const statusAfterStop = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('After Stop click:', { timerNumAfterStop, statusAfterStop });
  if (timerNumAfterStop !== '0.0s / 2.5s' || !statusAfterStop.includes('Sẵn sàng')) {
    throw new Error('TEST 2 FAILED: Drill was not properly reset after stop click.');
  }
  console.log('✅ TEST 2 PASSED: Stop button cleanly resets the drill.');

  // TEST 3: Switch Audio during Phase 1 (Teacher Audio)
  console.log('\n--- TEST 3: Switching audio during Phase 1 ---');
  // Start drill BÒ
  await page.evaluate(() => {
    window.triggerDrill('O', 'BÒ', 's3_y_pair_o');
  });
  await new Promise(r => setTimeout(r, 600));

  // While BÒ audio is playing, user plays Part I Lim intro
  console.log('User switches to Part I audio while drill was playing...');
  await page.evaluate(() => {
    window.playAudio('s1_lim_intro');
  });
  await new Promise(r => setTimeout(r, 300));

  const statusAfterSwitch = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('Status after audio switch:', statusAfterSwitch);
  if (!statusAfterSwitch.includes('Sẵn sàng')) {
    throw new Error('TEST 3 FAILED: Drill should be cancelled when user plays another audio track.');
  }

  await new Promise(r => setTimeout(r, 500));
  const timerNumPhase1 = await page.$eval('#drill-timer-num', el => el.innerText);
  if (timerNumPhase1 !== '0.0s / 2.5s') {
    throw new Error('TEST 3 FAILED: Drill entered countdown unexpectedly after another audio ended! Timer: ' + timerNumPhase1);
  }
  console.log('✅ TEST 3 PASSED: No phantom repeat countdown after audio switch.');

  // TEST 4: Switch Audio during Phase 2 (Countdown) -> Verify NO RUNAWAY INTERVAL
  console.log('\n--- TEST 4: Switching audio during Countdown (Verify no runaway timer > 2.5s) ---');
  await page.evaluate(() => {
    window.triggerDrill('O', 'BÒ', 's3_y_pair_o');
  });

  console.log('Waiting for teacher audio to finish...');
  await page.waitForFunction(() => {
    const tag = document.getElementById('drill-status-tag');
    return tag && tag.innerText.includes('ĐẾN LƯỢT BẠN');
  }, { timeout: 10000 });

  console.log('Countdown active! Waiting 800ms to be halfway through...');
  await new Promise(r => setTimeout(r, 800));
  const midTimer = await page.$eval('#drill-timer-num', el => el.innerText);
  console.log('Mid-countdown timer:', midTimer);

  // Now, user clicks another track (e.g. Vowel Ô sound)
  console.log('User clicks another track while countdown is in progress!');
  await page.evaluate(() => {
    window.playAudio('s2_nhung_oe_sound');
  });

  // Wait 4 seconds (longer than original 2.5s total).
  // If there was a runaway interval, it would have ticked up to 4.0s or 5.0s / 2.5s!
  console.log('Waiting 4 seconds to observe if any runaway interval exists...');
  await new Promise(r => setTimeout(r, 4000));

  const timerAfter4s = await page.$eval('#drill-timer-num', el => el.innerText);
  const statusAfter4s = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('Timer after 4s:', timerAfter4s, '| Status:', statusAfter4s);

  if (timerAfter4s !== '0.0s / 2.5s') {
    throw new Error('TEST 4 FAILED: Runaway interval detected! Timer value is: ' + timerAfter4s);
  }
  console.log('✅ TEST 4 PASSED: Timer cleanly stopped and never exceeded 2.5s or ran away!');

  // TEST 5: Full Shadowing Flow cancellation safety
  console.log('\n--- TEST 5: Full Shadowing Flow Cancellation ---');
  await page.evaluate(() => {
    window.startFullShadowing();
  });
  await new Promise(r => setTimeout(r, 400));

  console.log('Cancelling Full Flow via stopAndResetDrill...');
  await page.evaluate(() => {
    window.stopAndResetDrill(false);
  });

  await new Promise(r => setTimeout(r, 3000));
  const fullFlowStatus = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('Status after cancelled full flow:', fullFlowStatus);
  if (!fullFlowStatus.includes('Sẵn sàng')) {
    throw new Error('TEST 5 FAILED: Full flow steps fired after cancellation! Status: ' + fullFlowStatus);
  }
  console.log('✅ TEST 5 PASSED: Full Shadowing flow chain cleanly aborted without lingering timeouts.');

  // TEST 6: Normal Drill runs to 2.5s / 2.5s and finishes gracefully
  console.log('\n--- TEST 6: Complete Normal Drill ---');
  await page.evaluate(() => {
    window.triggerDrill('O', 'BÒ', 's3_y_pair_o');
  });

  await page.waitForFunction(() => {
    const tag = document.getElementById('drill-status-tag');
    return tag && tag.innerText.includes('ĐẾN LƯỢT BẠN');
  }, { timeout: 8000 });

  await page.waitForFunction(() => {
    const tag = document.getElementById('drill-status-tag');
    return tag && tag.innerText.includes('Hoàn thành');
  }, { timeout: 5000 });

  const finalTimer = await page.$eval('#drill-timer-num', el => el.innerText);
  const finalStatus = await page.$eval('#drill-status-tag', el => el.innerText);
  console.log('Completed Drill:', { finalTimer, finalStatus });
  if (finalTimer !== '2.5s / 2.5s') {
    throw new Error('TEST 6 FAILED: Final timer should be exactly 2.5s / 2.5s, got: ' + finalTimer);
  }
  console.log('✅ TEST 6 PASSED: Completed drill shows exact 2.5s / 2.5s with victory prompt.');

  // Take screenshot of finished state
  await page.screenshot({ path: 'screenshot_shadowing_verified.png' });
  console.log('📸 Screenshot saved to screenshot_shadowing_verified.png');

  await browser.close();
  console.log('\n🎉 ALL TESTS PASSED WITH ZERO TECHNICAL ERRORS!');
}

runTests().catch(err => {
  console.error('❌ Test execution error:', err);
  process.exit(1);
});
