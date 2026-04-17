/**
 * 测试4：mnsv2 已注册成功，现在测试正确的调用方式
 *
 * 基于 test3 的成功环境，添加：
 * 1. document.cookie 设置（a1 等）
 * 2. 正确的 mnsv2 调用参数
 * 3. 完整的签名流程测试
 */

const https = require('https');
const nodeCrypto = require('crypto');

const VENDOR_URL = 'https://fe-static.xhscdn.com/formula-static/xhs-pc-web/public/resource/js/vendor-dynamic.995533cf.js';

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : require('http');
    const req = mod.get(url, {
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
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('timeout')); });
  });
}

function extractSeccoreCode(vendorScript) {
  const startMarker = '__makeTemplateObject(["';
  let startIdx = vendorScript.indexOf(startMarker);
  if (startIdx === -1) return null;
  const cookedStart = startIdx + startMarker.length;
  const separator = '"],["';
  const sepIdx = vendorScript.indexOf(separator, cookedStart);
  if (sepIdx === -1) return null;
  const rawStart = sepIdx + separator.length;
  const rawEnd = vendorScript.indexOf('"])', rawStart);
  if (rawEnd === -1) return null;
  try {
    return JSON.parse('"' + vendorScript.substring(rawStart, rawEnd) + '"');
  } catch (e) { return null; }
}

(async () => {
  const _console = console;
  const _setTimeout = setTimeout;
  const _clearTimeout = clearTimeout;
  const _setInterval = setInterval;
  const _clearInterval = clearInterval;
  const _Buffer = Buffer;
  const _process = process;

  _console.error('[test4] 下载 vendor-dynamic.js...');
  const vendorScript = await fetchUrl(VENDOR_URL);
  _console.error(`[test4] 大小: ${vendorScript.length}`);

  const code = extractSeccoreCode(vendorScript);
  if (!code) { _console.error('[test4] 提取失败'); _process.exit(1); }
  _console.error(`[test4] 代码长度: ${code.length}`);

  // === 隐藏 Node.js ===
  const chromeUA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36';
  Object.defineProperty(globalThis, 'navigator', {
    value: {
      userAgent: chromeUA, platform: 'Win32', language: 'zh-CN', languages: ['zh-CN', 'zh'],
      hardwareConcurrency: 8, maxTouchPoints: 0, cookieEnabled: true, onLine: true,
      plugins: { length: 0 }, connection: { effectiveType: '4g', downlink: 10, rtt: 50 },
      webdriver: false, vendor: 'Google Inc.',
      appVersion: chromeUA.replace('Mozilla/', ''), product: 'Gecko', productSub: '20030107',
      appCodeName: 'Mozilla', appName: 'Netscape', mimeTypes: { length: 0 },
      doNotTrack: null, getBattery: () => Promise.resolve({ charging: true, level: 1 }),
      javaEnabled: () => false, sendBeacon: () => true,
    },
    writable: true, configurable: true, enumerable: true
  });

  const nodeGlobals = ['process', 'Buffer', 'require', 'module', 'exports', '__dirname', '__filename', 'global'];
  const saved = {};
  for (const name of nodeGlobals) {
    if (name in globalThis) {
      saved[name] = globalThis[name];
      try { Object.defineProperty(globalThis, name, { value: undefined, writable: true, configurable: true }); }
      catch(e) { try { delete globalThis[name]; } catch(e2) {} }
    }
  }

  // === 浏览器环境 ===
  const perfStart = Date.now();
  globalThis.window = globalThis;
  globalThis.self = globalThis;
  globalThis.top = globalThis;

  globalThis.performance = {
    now: () => Date.now() - perfStart,
    timing: { navigationStart: perfStart - 5000 },
    getEntriesByType: () => [], mark: () => {}, measure: () => {},
  };

  globalThis.crypto = {
    getRandomValues: (arr) => {
      const bytes = nodeCrypto.randomBytes(arr.byteLength);
      const view = new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength);
      for (let i = 0; i < view.length; i++) view[i] = bytes[i];
      return arr;
    },
    subtle: {
      digest: async (algo, data) => {
        const name = algo.replace('-', '').toLowerCase();
        const hash = nodeCrypto.createHash(name === 'sha256' ? 'sha256' : name === 'sha1' ? 'sha1' : 'md5');
        hash.update(new Uint8Array(data));
        const result = hash.digest();
        return result.buffer.slice(result.byteOffset, result.byteOffset + result.byteLength);
      },
    },
    randomUUID: () => nodeCrypto.randomUUID(),
  };

  // ★★★ 关键：设置 cookie（包含 a1）★★★
  const a1 = '198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow85000085579';
  const webId = 'fc4fb0dccb1a480d5f17359394c861d7';
  const cookieStr = `a1=${a1}; webId=${webId}; xsecappid=xhs-pc-web; webBuild=5.11.0`;

  globalThis.document = {
    createElement: (tag) => {
      if (tag === 'canvas') {
        return {
          getContext: (type) => {
            if (type === '2d') {
              return {
                fillText: () => {}, measureText: () => ({ width: 42 }),
                fillRect: () => {}, arc: () => {}, stroke: () => {},
                beginPath: () => {}, closePath: () => {}, fill: () => {},
                canvas: { toDataURL: () => 'data:image/png;base64,iVBOR' },
                fillStyle: '', font: '', textBaseline: '',
              };
            }
            return {
              getExtension: () => null,
              getParameter: (p) => p === 37445 ? 'Google Inc.' : p === 37446 ? 'ANGLE (Intel)' : '',
              getSupportedExtensions: () => [],
              createBuffer: () => ({}), bindBuffer: () => {},
              bufferData: () => {}, createProgram: () => ({}),
              createShader: () => ({}), shaderSource: () => {},
              compileShader: () => {}, attachShader: () => {},
              linkProgram: () => {}, useProgram: () => {},
              drawArrays: () => {},
            };
          },
          toDataURL: () => 'data:image/png;base64,iVBOR',
          width: 300, height: 150,
        };
      }
      return {
        style: {}, appendChild: () => {}, setAttribute: () => {},
        addEventListener: () => {}, removeEventListener: () => {},
        innerHTML: '', textContent: '', offsetHeight: 0, offsetWidth: 0,
        getBoundingClientRect: () => ({ top: 0, left: 0, bottom: 0, right: 0, width: 0, height: 0 }),
      };
    },
    createElementNS: (ns, tag) => globalThis.document.createElement(tag),
    createTextNode: (text) => ({ textContent: text }),
    addEventListener: () => {}, removeEventListener: () => {},
    getElementById: () => null, querySelector: () => null,
    querySelectorAll: () => [], getElementsByTagName: () => [],
    getElementsByClassName: () => [],
    cookie: cookieStr,  // ★★★ 设置 cookie ★★★
    title: '', referrer: 'https://www.xiaohongshu.com/',
    documentElement: { style: {}, getAttribute: () => null },
    body: { appendChild: () => {}, removeChild: () => {}, style: {} },
    head: { appendChild: () => {} },
    location: { href: 'https://www.xiaohongshu.com/', hostname: 'www.xiaohongshu.com', protocol: 'https:', origin: 'https://www.xiaohongshu.com' },
    readyState: 'complete', visibilityState: 'visible', hidden: false,
  };

  globalThis.location = globalThis.document.location;

  const createStorage = () => {
    const store = {};
    return {
      getItem: (k) => store[k] || null,
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: (k) => { delete store[k]; },
      clear: () => { for (const k in store) delete store[k]; },
      get length() { return Object.keys(store).length; },
      key: (i) => Object.keys(store)[i] || null,
    };
  };
  globalThis.localStorage = createStorage();
  globalThis.sessionStorage = createStorage();
  globalThis.screen = { width: 1920, height: 1080, availWidth: 1920, availHeight: 1040, colorDepth: 24, pixelDepth: 24 };
  globalThis.chrome = { runtime: {}, webstore: {} };
  globalThis.MutationObserver = class { constructor(cb) {} observe() {} disconnect() {} takeRecords() { return []; } };
  globalThis.IntersectionObserver = class { constructor(cb) {} observe() {} disconnect() {} };
  globalThis.ResizeObserver = class { constructor(cb) {} observe() {} disconnect() {} };
  globalThis.Image = class { constructor() { this.onload = null; } set src(v) { if (this.onload) _setTimeout(() => this.onload(), 0); } };
  globalThis.Event = class Event { constructor(type) { this.type = type; } };
  globalThis.CustomEvent = class extends globalThis.Event { constructor(type, opts) { super(type); this.detail = opts?.detail; } };
  globalThis.history = { pushState: () => {}, replaceState: () => {} };
  globalThis.requestAnimationFrame = (cb) => _setTimeout(cb, 16);
  globalThis.cancelAnimationFrame = (id) => _clearTimeout(id);
  globalThis.requestIdleCallback = (cb) => _setTimeout(() => cb({ didTimeout: false, timeRemaining: () => 50 }), 0);
  globalThis.getComputedStyle = () => new Proxy({}, { get: () => '' });
  globalThis.matchMedia = () => ({ matches: false, addListener: () => {}, removeListener: () => {} });
  globalThis.btoa = (s) => _Buffer.from(s, 'binary').toString('base64');
  globalThis.atob = (s) => _Buffer.from(s, 'base64').toString('binary');
  globalThis.InstallTrigger = undefined;
  globalThis.Blob = class { constructor(parts, opts) { this.size = 0; this.type = opts?.type || ''; } };
  globalThis.Worker = class { constructor() {} postMessage() {} terminate() {} };
  globalThis.MessageChannel = class { constructor() { this.port1 = { onmessage: null, postMessage: () => {} }; this.port2 = { onmessage: null, postMessage: () => {} }; } };
  globalThis.AbortController = class { constructor() { this.signal = { aborted: false, addEventListener: () => {} }; } abort() { this.signal.aborted = true; } };

  globalThis.XMLHttpRequest = class {
    constructor() {
      this.readyState = 0; this.status = 0; this.responseText = ''; this.response = '';
      this.onreadystatechange = null; this.onload = null; this.onerror = null; this._headers = {};
    }
    open(method, url) { this._method = method; this._url = url; this.readyState = 1; }
    setRequestHeader(k, v) { this._headers[k] = v; }
    getResponseHeader() { return null; }
    getAllResponseHeaders() { return ''; }
    send(body) {
      this.status = 200; this.responseText = '{}'; this.response = '{}'; this.readyState = 4;
      const self = this;
      if (this.onreadystatechange) _setTimeout(() => self.onreadystatechange(), 0);
      if (this.onload) _setTimeout(() => self.onload(), 0);
    }
    abort() {}
  };

  globalThis.fetch = () => Promise.resolve({
    ok: true, status: 200, text: () => Promise.resolve('{}'),
    json: () => Promise.resolve({}), headers: { get: () => null },
  });

  // === 执行 seccore ===
  _console.error('[test4] 执行 seccore 代码...');
  try {
    const fn = new Function(code);
    fn();
  } catch (e) {
    _console.error(`[test4] 执行错误: ${e.message}`);
  }

  _console.error(`[test4] mnsv2: ${typeof globalThis.mnsv2}`);

  if (typeof globalThis.mnsv2 !== 'function') {
    _console.error('[test4] mnsv2 未注册');
    _process.exit(1);
  }

  _console.error('[test4] mnsv2 注册成功!');

  // === 测试不同的调用方式 ===
  const testUrl = '/api/sns/web/v2/comment/page?note_id=699dd0b1000000001d024fe6&cursor=&top_comment_id=&image_formats=jpg,webp,avif';

  // 方式1：三参数 mnsv2(url, hash1, hash2)
  _console.error('\n[test4] === 测试1: mnsv2(url, md5, md5) ===');
  try {
    const md5 = nodeCrypto.createHash('md5').update(testUrl).digest('hex');
    const r1 = globalThis.mnsv2(testUrl, md5, md5);
    _console.error(`[test4] 结果: ${String(r1).substring(0, 100)}`);
    _console.error(`[test4] 长度: ${String(r1).length}`);
  } catch (e) {
    _console.error(`[test4] 错误: ${e.message}`);
  }

  // 方式2：两参数 mnsv2(url, hash)
  _console.error('\n[test4] === 测试2: mnsv2(url, md5) ===');
  try {
    const md5 = nodeCrypto.createHash('md5').update(testUrl).digest('hex');
    const r2 = globalThis.mnsv2(testUrl, md5);
    _console.error(`[test4] 结果: ${String(r2).substring(0, 100)}`);
    _console.error(`[test4] 长度: ${String(r2).length}`);
  } catch (e) {
    _console.error(`[test4] 错误: ${e.message}`);
  }

  // 方式3：单参数 mnsv2(url)
  _console.error('\n[test4] === 测试3: mnsv2(url) ===');
  try {
    const r3 = globalThis.mnsv2(testUrl);
    _console.error(`[test4] 结果: ${String(r3).substring(0, 100)}`);
    _console.error(`[test4] 长度: ${String(r3).length}`);
  } catch (e) {
    _console.error(`[test4] 错误: ${e.message}`);
  }

  // 方式4：检查 mnsv2 的参数个数
  _console.error(`\n[test4] mnsv2.length (形参数): ${globalThis.mnsv2.length}`);
  _console.error(`[test4] mnsv2.toString() 前200字符: ${globalThis.mnsv2.toString().substring(0, 200)}`);

  // 方式5：列出所有新注册的全局函数，看看有没有其他有用的
  const allFuncs = Object.keys(globalThis).filter(k => {
    try { return typeof globalThis[k] === 'function' && k.startsWith('_') && k.length > 5; } catch(e) { return false; }
  });
  _console.error(`\n[test4] 所有 _ 开头函数: ${allFuncs.join(', ')}`);

  // 恢复
  for (const [name, val] of Object.entries(saved)) globalThis[name] = val;
  process.exit(0);
})();
