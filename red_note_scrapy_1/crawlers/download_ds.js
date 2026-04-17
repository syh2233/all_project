// 下载 DS 脚本并保存到文件，同时分析其内容
const https = require('https');
const fs = require('fs');
const path = require('path');

const DS_URL = 'https://as.xiaohongshu.com/api/sec/v1/ds?appId=xhs-pc-web';

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://www.xiaohongshu.com/',
      }
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchUrl(res.headers.location).then(resolve).catch(reject);
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('timeout')); });
  });
}

(async () => {
  console.log('下载 DS 脚本...');
  const script = await fetchUrl(DS_URL);
  console.log(`大小: ${script.length} 字符`);

  // 保存到文件
  const outPath = path.join(__dirname, 'ds_script.js');
  fs.writeFileSync(outPath, script, 'utf-8');
  console.log(`已保存到: ${outPath}`);

  // 分析关键模式
  console.log('\n=== 分析 ===');
  console.log(`包含 mnsv2: ${script.includes('mnsv2')}`);
  console.log(`包含 _AUuXfEG27Xa3x: ${script.includes('_AUuXfEG27Xa3x')}`);
  console.log(`包含 _BHjFmfUMEtxhI: ${script.includes('_BHjFmfUMEtxhI')}`);
  console.log(`包含 scripting: ${script.includes('scripting')}`);
  console.log(`包含 fetch: ${script.includes('fetch')}`);
  console.log(`包含 XMLHttpRequest: ${script.includes('XMLHttpRequest')}`);
  console.log(`包含 6545c70e: ${script.includes('6545c70e')}`);
  console.log(`包含 xhscdn: ${script.includes('xhscdn')}`);

  // 搜索 URL 模式
  const urlMatches = script.match(/https?:\/\/[^\s'"]+/g) || [];
  console.log(`\nURL 模式: ${urlMatches.length}`);
  urlMatches.forEach(u => console.log(`  ${u.substring(0, 100)}`));

  // 搜索 window 赋值
  const windowAssigns = [];
  let idx = 0;
  while ((idx = script.indexOf('window[', idx)) !== -1) {
    windowAssigns.push(script.substring(idx, Math.min(idx + 80, script.length)));
    idx++;
    if (windowAssigns.length > 10) break;
  }
  console.log(`\nwindow[] 赋值: ${windowAssigns.length}`);
  windowAssigns.forEach(w => console.log(`  ${w}`));

  // 搜索 eval/Function 调用
  console.log(`\n包含 eval: ${script.includes('eval(')}`);
  console.log(`包含 new Function: ${script.includes('new Function')}`);
  console.log(`包含 Function(: ${script.includes('Function(')}`);

  // 前200字符
  console.log(`\n前200字符:\n${script.substring(0, 200)}`);
  console.log(`\n后200字符:\n${script.substring(script.length - 200)}`);
})();
