import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 1000));
  
  const before = await page.$eval('#audio-track-title', el => el.innerText);
  console.log('Before click:', before);
  
  const err = await page.evaluate(() => {
    try {
      const b = document.getElementById('btn-quick-o');
      console.log('triggerMascotBounce exists?', typeof window.triggerMascotBounce);
      b.click();
      return null;
    } catch(e) {
      return e.stack;
    }
  });
  console.log('Click error:', err);
  
  const after = await page.$eval('#audio-track-title', el => el.innerText);
  console.log('After click:', after);

  const btn = await page.$('#btn-quick-oe');
  await btn.click();
  await new Promise(r => setTimeout(r, 300));
  const afterOE = await page.$eval('#audio-track-title', el => el.innerText);
  console.log('After puppeteer click OE:', afterOE);
  
  await browser.close();
})();
