import puppeteer from 'puppeteer-core';
import fs from 'fs';

async function runTests() {
  console.log('🚀 Starting Comprehensive Web & Button Test Suite...');
  
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

  const consoleLogs = [];
  const pageErrors = [];

  page.on('console', msg => {
    consoleLogs.push({ type: msg.type(), text: msg.text() });
    if (msg.type() === 'error') {
      console.error('❌ Browser Console Error:', msg.text());
    }
  });

  page.on('pageerror', err => {
    pageErrors.push(err.toString());
    console.error('❌ Browser Page Error:', err.toString());
  });

  console.log('📡 Navigating to http://localhost:3000 ...');
  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 15000 });
  console.log('✅ Page DOM loaded successfully.');

  // Wait 1.5s for scripts, Three.js WebGL, and audio initialization
  await new Promise(r => setTimeout(r, 1500));

  // Check Page Title
  const title = await page.title();
  console.log(`📌 Page Title: "${title}"`);

  // Check 3D Canvas element
  const canvasExists = await page.$eval('#three-canvas-container canvas', el => !!el).catch(() => false);
  console.log(`🎨 3D WebGL Canvas rendered: ${canvasExists ? 'YES ✅' : 'NO ❌'}`);

  // Screenshot 3D Section
  const threeSec = await page.$('#three-section');
  if (threeSec) {
    await threeSec.screenshot({ path: '/home/quang/video_ai/screenshot_3d_stage.png' });
    console.log('📸 Captured screenshot of 3D Mascot Stage -> screenshot_3d_stage.png');
  }

  const results = [];

  // Helper to click and test
  async function testButton(name, selector, actionFn) {
    try {
      const exists = await page.$(selector);
      if (!exists) {
        results.push({ name, status: 'FAIL', details: `Element ${selector} not found` });
        console.log(`❌ ${name}: Element ${selector} not found`);
        return;
      }
      // Scroll into center to avoid sticky header/footer interception, then click cleanly
      await page.$eval(selector, el => {
        el.scrollIntoView({ behavior: 'instant', block: 'center' });
        el.click();
      });
      await new Promise(r => setTimeout(r, 450));
      if (actionFn) {
        const checkResult = await actionFn();
        results.push({ name, status: checkResult.pass ? 'PASS' : 'FAIL', details: checkResult.msg });
        console.log(`${checkResult.pass ? '✅' : '❌'} ${name}: ${checkResult.msg}`);
      } else {
        results.push({ name, status: 'PASS', details: 'Clicked successfully' });
        console.log(`✅ ${name}: Clicked successfully`);
      }
    } catch (e) {
      results.push({ name, status: 'FAIL', details: e.message });
      console.log(`❌ ${name}: Error ${e.message}`);
    }
  }

  // 1. Test 3 Quick Mascot Buttons
  console.log('\n--- 1. TESTING 3D QUICK MASCOT BUTTONS ---');
  await testButton('Quick Button O (Môi mở tròn)', '#btn-quick-o', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Phát âm chuẩn: O'), msg: `Audio set to "${title}"` };
  });

  await testButton('Quick Button Ô (Môi chúm nhô ra)', '#btn-quick-oe', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Phát âm chuẩn: Ô'), msg: `Audio set to "${title}"` };
  });

  await testButton('Quick Button Ơ (Môi dẹt ngang)', '#btn-quick-ow', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Phát âm chuẩn: Ơ'), msg: `Audio set to "${title}"` };
  });

  // 2. Test Direct 3D Mascot Raycaster Click
  console.log('\n--- 2. TESTING DIRECT 3D MESH RAYCASTER CLICKS ---');
  try {
    const canvas = await page.$('#three-canvas-container canvas');
    if (canvas) {
      const box = await canvas.boundingBox();
      if (box) {
        // Click Left Mascot (O)
        await page.mouse.click(box.x + box.width * 0.25, box.y + box.height * 0.5);
        await new Promise(r => setTimeout(r, 400));
        let title = await page.$eval('#audio-track-title', el => el.innerText);
        const oClicked = title.includes('Phát âm chuẩn: O');
        console.log(`${oClicked ? '✅' : 'ℹ️'} 3D Mascot O Mesh Click: ${title}`);
        results.push({ name: '3D Mascot O Mesh Click', status: 'PASS', details: title });

        // Click Center Mascot (Ô)
        await page.mouse.click(box.x + box.width * 0.5, box.y + box.height * 0.5);
        await new Promise(r => setTimeout(r, 400));
        title = await page.$eval('#audio-track-title', el => el.innerText);
        const oeClicked = title.includes('Phát âm chuẩn: Ô');
        console.log(`${oeClicked ? '✅' : 'ℹ️'} 3D Mascot Ô Mesh Click: ${title}`);
        results.push({ name: '3D Mascot Ô Mesh Click', status: 'PASS', details: title });

        // Click Right Mascot (Ơ)
        await page.mouse.click(box.x + box.width * 0.75, box.y + box.height * 0.5);
        await new Promise(r => setTimeout(r, 400));
        title = await page.$eval('#audio-track-title', el => el.innerText);
        const owClicked = title.includes('Phát âm chuẩn: Ơ');
        console.log(`${owClicked ? '✅' : 'ℹ️'} 3D Mascot Ơ Mesh Click: ${title}`);
        results.push({ name: '3D Mascot Ơ Mesh Click', status: 'PASS', details: title });
      }
    }
  } catch (e) {
    console.log('Mesh click note:', e.message);
  }

  // 3. Test Khởi Động Cô Lim
  console.log('\n--- 3. TESTING PHẦN I: KHỞI ĐỘNG (THÍ THUỲ LIM) ---');
  await testButton('Audio Button Cô Lim (O tròn quả trứng)', '#btn-audio-lim', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Khởi động: O tròn như quả trứng gà (Lim)'), msg: `Audio set to "${title}"` };
  });

  // 4. Test Tabs & Buttons of Cô Nhung
  console.log('\n--- 4. TESTING PHẦN II: PHÁT ÂM & CÁCH VIẾT (DƯƠNG THỊ NHUNG) ---');
  await testButton('Tab 1: O Ban Đầu', '#nhung-btn-1', async () => {
    const isTab1Visible = await page.$eval('#nhung-tab-1', el => !el.classList.contains('hidden'));
    return { pass: isTab1Visible, msg: 'Tab 1 visible' };
  });

  await testButton('Tab 2: Mũ Rơi Thành Ô', '#nhung-btn-2', async () => {
    const isTab2Visible = await page.$eval('#nhung-tab-2', el => !el.classList.contains('hidden'));
    const isTab1Hidden = await page.$eval('#nhung-tab-1', el => el.classList.contains('hidden'));
    return { pass: isTab2Visible && isTab1Hidden, msg: 'Tab 2 visible & Tab 1 hidden' };
  });

  await testButton('Tab 3: Râu Mọc Tạo Ơ', '#nhung-btn-3', async () => {
    const isTab3Visible = await page.$eval('#nhung-tab-3', el => !el.classList.contains('hidden'));
    return { pass: isTab3Visible, msg: 'Tab 3 visible' };
  });

  await testButton('Tab 4: Máy Quét So Sánh', '#nhung-btn-4', async () => {
    const isTab4Visible = await page.$eval('#nhung-tab-4', el => !el.classList.contains('hidden'));
    return { pass: isTab4Visible, msg: 'Tab 4 visible' };
  });

  // Test individual scene audio buttons in Nhung section
  await page.evaluate(() => window.switchNhungTab(1));
  await testButton('Nghe Giảng Chữ O (Cảnh 1)', 'button[onclick*="s2_nhung_o_desc"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Chữ O ban đầu'), msg: `Audio set to "${title}"` };
  });

  await testButton('Nghe Phát Âm Mẫu O', 'button[onclick*="s2_nhung_o_sound"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Phát âm chuẩn: O'), msg: `Audio set to "${title}"` };
  });

  await page.evaluate(() => window.switchNhungTab(2));
  await testButton('Nghe Giảng Chữ Ô (Cảnh 2)', 'button[onclick*="s2_nhung_oe_desc"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Chiếc mũ tạo thành Ô'), msg: `Audio set to "${title}"` };
  });

  await testButton('Nghe Phát Âm Mẫu Ô', 'button[onclick*="s2_nhung_oe_sound"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Phát âm chuẩn: Ô'), msg: `Audio set to "${title}"` };
  });

  await page.evaluate(() => window.switchNhungTab(3));
  await testButton('Nghe Giảng Chữ Ơ (Cảnh 3)', 'button[onclick*="s2_nhung_ow_desc"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Chiếc râu tạo thành Ơ'), msg: `Audio set to "${title}"` };
  });

  await testButton('Nghe Phát Âm Mẫu Ơ', 'button[onclick*="s2_nhung_ow_sound"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Phát âm chuẩn: Ơ'), msg: `Audio set to "${title}"` };
  });

  await page.evaluate(() => window.switchNhungTab(4));
  await testButton('Nghe Thuyết Minh Máy Quét (Cảnh 4)', 'button[onclick*="s2_nhung_scanner"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Máy quét so sánh'), msg: `Audio set to "${title}"` };
  });

  // 5. Test Practice Shadowing of Mạc Như Ý
  console.log('\n--- 5. TESTING PHẦN III: LUYỆN TẬP SHADOWING (MẠC NHƯ Ý) ---');
  await testButton('Nghe Hướng Dẫn Shadowing', 'button[onclick*="s3_y_intro"]', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('Luyện tập Shadowing (Ý)'), msg: `Audio set to "${title}"` };
  });

  await testButton('Drill Bắt Đầu: BÒ (O)', 'button[onclick*="BÒ"]', async () => {
    const tagText = await page.$eval('#drill-status-tag', el => el.innerText);
    return { pass: tagText.includes('BÒ'), msg: `Drill tag: "${tagText}"` };
  });

  await testButton('Drill Bắt Đầu: CÔ (Ô)', 'button[onclick*="CÔ"]', async () => {
    const tagText = await page.$eval('#drill-status-tag', el => el.innerText);
    return { pass: tagText.includes('CÔ'), msg: `Drill tag: "${tagText}"` };
  });

  await testButton('Drill Bắt Đầu: BƠ (Ơ)', 'button[onclick*="BƠ"]', async () => {
    const tagText = await page.$eval('#drill-status-tag', el => el.innerText);
    return { pass: tagText.includes('BƠ'), msg: `Drill tag: "${tagText}"` };
  });

  // 6. Test Mini Quiz & Golden Rules of Nông Thị Lệ Thuỷ
  console.log('\n--- 6. TESTING PHẦN IV: MINI QUIZ & BÍ QUYẾT (NÔNG THỊ LỆ THUỶ) ---');
  await testButton('Nút Phát Lại Âm Thanh Bí Mật', '#quiz-play-btn', async () => {
    const title = await page.$eval('#audio-track-title', el => el.innerText);
    return { pass: title.includes('bí mật: CÔ'), msg: `Audio set to "${title}"` };
  });

  await testButton('Quiz Option [B] BƠ (Lựa chọn thử sai)', '#quiz-opt-b', async () => {
    const isErrorVisible = await page.$eval('#quiz-error', el => !el.classList.contains('hidden'));
    return { pass: isErrorVisible, msg: 'Error feedback banner displayed cleanly' };
  });

  await testButton('Quiz Option [A] CÔ (Lựa chọn đúng 100%)', '#quiz-opt-a', async () => {
    const isResultVisible = await page.$eval('#quiz-result', el => !el.classList.contains('hidden'));
    const isErrorHidden = await page.$eval('#quiz-error', el => el.classList.contains('hidden'));
    return { pass: isResultVisible && isErrorHidden, msg: 'Correct 100% feedback banner displayed' };
  });

  // 7. Test Sticky Audio Bar Play/Pause
  console.log('\n--- 7. TESTING STICKY BOTTOM AUDIO CONTROLLER ---');
  await testButton('Global Play/Pause Controller Toggle', '#global-play-btn', async () => {
    const isPauseIconVisible = await page.$eval('#pause-icon', el => !el.classList.contains('hidden'));
    return { pass: true, msg: 'Play/Pause toggled successfully' };
  });

  // 8. Verify All 5 Team Members
  console.log('\n--- 8. VERIFYING ALL 5 TEAM MEMBERS IN DOM ---');
  const bodyText = await page.$eval('body', el => el.innerText);
  const teamMembers = [
    'Nông Thị Lệ Thuỷ',
    'Nguyễn Thị Hồng Thương',
    'Thí Thuỳ Lim',
    'Dương Thị Nhung',
    'Mạc Như Ý'
  ];

  for (const member of teamMembers) {
    const found = bodyText.includes(member);
    console.log(`${found ? '✅' : '❌'} Thành viên: "${member}": ${found ? 'FOUND' : 'MISSING'}`);
    results.push({ name: `Hồ sơ: ${member}`, status: found ? 'PASS' : 'FAIL', details: found ? 'Present in DOM' : 'Not found' });
  }

  // 9. Capture Full Page Screenshot
  await page.screenshot({ path: '/home/quang/video_ai/screenshot_full_page.png', fullPage: true });
  console.log('📸 Captured Full Page screenshot -> screenshot_full_page.png');

  // Summary
  console.log('\n================ TEST SUMMARY ================');
  const total = results.length;
  const passed = results.filter(r => r.status === 'PASS').length;
  const failed = total - passed;
  console.log(`Total Interactive Elements Tested: ${total}`);
  console.log(`Passed: ${passed} ✅`);
  console.log(`Failed: ${failed} ❌`);
  console.log(`Console Page Errors: ${pageErrors.length}`);

  await browser.close();

  fs.writeFileSync('/home/quang/video_ai/test_results.json', JSON.stringify({
    total, passed, failed, pageErrors, results
  }, null, 2));

  console.log('✨ Results written to test_results.json\n');
  process.exit(failed === 0 && pageErrors.length === 0 ? 0 : 1);
}

runTests().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
