/**
 * Node.js 签名服务 - 通过执行小红书 signUrl 脚本生成真实 XYW_ 签名
 *
 * 用法:
 *   node node_sign.js <api_url>
 *   node node_sign.js "/api/sns/web/v2/comment/sub/page?note_id=xxx&cursor="
 *
 * 输出 JSON: {"xs": "XYW_...", "xt": "1234567890"}
 */

const https = require('https');
const http = require('http');
const vm = require('vm');

// signUrl 脚本 URL（从 sdt_source_storage_key 获取）
const SIGN_URL = 'https://fe-static.xhscdn.com/as/v1/f218/a15/public/04b29480233f4def5c875875b6bdc3b1.js';

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function setupBrowserMocks() {
  global.window = global;
  global.self = global;

  global.document = {
    createElement: (tag) => {
      if (tag === 'canvas') {
        return {
          getContext: () => ({
            fillText: () => {}, measureText: () => ({ width: 0 }),
            fillRect: () => {}, arc: () => {}, stroke: () => {},
            canvas: { toDataURL: () => 'data:image/png;base64,' },
          }),
          toDataURL: () => 'data:image/png;base64,',
          width: 0, height: 0,
        };
      }
      return { style: {}, appendChild: () => {}, setAttribute: () => {} };
    },
    addEventListener: () => {}, removeEventListener: () => {},
    getElementById: () => null, querySelector: () => null,
    querySelectorAll: () => [], cookie: '',
    body: { appendChild: () => {}, removeChild: () => {} },
    head: { appendChild: () => {} },
    documentElement: { style: {} },
  };

  global.performance = {
    now: () => Date.now(),
    timing: { navigationStart: Date.now() - 5000 },
    getEntriesByType: () => [],
  };

  global.MutationObserver = class { constructor() {} observe() {} disconnect() {} };

  const mkStore = () => {
    const s = {};
    return { getItem: k => s[k] || null, setItem: (k, v) => { s[k] = String(v); }, removeItem: k => { delete s[k]; } };
  };
  global.localStorage = mkStore();
  global.sessionStorage = mkStore();

  global.location = {
    href: 'https://www.xiaohongshu.com/explore',
    origin: 'https://www.xiaohongshu.com',
    protocol: 'https:', host: 'www.xiaohongshu.com',
    hostname: 'www.xiaohongshu.com', pathname: '/explore',
    search: '', hash: '',
  };

  global.navigator = {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    language: 'zh-CN', languages: ['zh-CN', 'zh', 'en'],
    platform: 'Win32', cookieEnabled: true,
    hardwareConcurrency: 8, maxTouchPoints: 0,
  };

  global.screen = { width: 1920, height: 1080, colorDepth: 24, availWidth: 1920, availHeight: 1040 };
  global.btoa = (str) => Buffer.from(str, 'binary').toString('base64');
  global.atob = (str) => Buffer.from(str, 'base64').toString('binary');
  global.XMLHttpRequest = class { open() {} send() {} setRequestHeader() {} };
  global.Image = class { set src(v) {} get width() { return 0; } get height() { return 0; } };
  global.requestAnimationFrame = (cb) => setTimeout(cb, 16);
  global.cancelAnimationFrame = (id) => clearTimeout(id);
}

function startServer(port) {
  const server = http.createServer(async (req, res) => {
    if (req.method === 'GET' && req.url.startsWith('/sign?')) {
      const params = new URL(req.url, 'http://localhost').searchParams;
      const apiUrl = params.get('url');
      if (!apiUrl) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Missing url parameter' }));
        return;
      }
      try {
        const result = global._webmsxyw(apiUrl, undefined);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ xs: result['X-s'], xt: String(result['X-t']) }));
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    } else if (req.method === 'GET' && req.url === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ok' }));
    } else {
      res.writeHead(404);
      res.end('Not Found');
    }
  });
  server.listen(port, '127.0.0.1', () => {
    console.log(JSON.stringify({ status: 'ready', port }));
  });
  return server;
}

async function main() {
  setupBrowserMocks();

  process.stderr.write('Downloading signUrl script...\n');
  const signScript = await fetchUrl(SIGN_URL);
  process.stderr.write(`signUrl script: ${signScript.length} bytes\n`);

  // 执行 signUrl 脚本（它会设置 global._webmsxyw）
  try {
    vm.runInThisContext(signScript, { filename: 'sign_script.js' });
  } catch (e) {
    process.stderr.write(`vm.runInThisContext error: ${e.message}\n`);
    // 回退到 eval
    try { eval(signScript); } catch (e2) {
      process.stderr.write(`eval error: ${e2.message}\n`);
    }
  }

  await new Promise(r => setTimeout(r, 500));

  if (typeof global._webmsxyw !== 'function') {
    process.stderr.write('Error: _webmsxyw not available\n');
    process.exit(1);
  }

  process.stderr.write('_webmsxyw loaded successfully\n');

  const args = process.argv.slice(2);
  if (args[0] === '--server') {
    startServer(parseInt(args[1]) || 5678);
  } else if (args.length > 0) {
    try {
      const result = global._webmsxyw(args[0], undefined);
      console.log(JSON.stringify({ xs: result['X-s'], xt: String(result['X-t']) }));
    } catch (e) {
      console.log(JSON.stringify({ error: e.message }));
      process.exit(1);
    }
  } else {
    console.error('Usage:');
    console.error('  node node_sign.js <api_url>          # Single sign');
    console.error('  node node_sign.js --server [port]    # HTTP server mode');
    process.exit(1);
  }
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
