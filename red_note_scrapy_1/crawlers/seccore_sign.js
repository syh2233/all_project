/**
 * seccore 签名服务 - 在 Node.js 中运行小红书 seccore 虚拟机生成真实 mnsv2 签名
 *
 * 原理：
 * 1. 下载 vendor-dynamic.js（包含 webpack 模块 41481 的 signV2Init）
 * 2. 提取 signV2Init 中 String.raw 模板的 seccore 代码（~251KB）
 * 3. 从 vendor-dynamic.js 中提取自定义 Base64 字母表、版本号等
 * 4. 在全局作用域中模拟浏览器环境（关键：crypto.getRandomValues + 隐藏 Node.js 特征）
 * 5. 执行 seccore 代码，注册 mnsv2
 * 6. 使用提取的 webpack 辅助函数构建完整 XYS_ 签名和 x-s-common
 *
 * 用法:
 *   node seccore_sign.js --server 5679          # HTTP 服务模式
 *   node seccore_sign.js "/api/sns/web/v2/..."  # 单次调用模式
 */

const _https = require('https');
const _http = require('http');
const _nodeCrypto = require('crypto');
const _Buffer = Buffer;
const _process = process;
const _console = console;
const _setTimeout = setTimeout;
const _clearTimeout = clearTimeout;
const _setInterval = setInterval;
const _clearInterval = clearInterval;
const _require = require;

const VENDOR_URL = 'https://fe-static.xhscdn.com/formula-static/xhs-pc-web/public/resource/js/vendor-dynamic.995533cf.js';

let _vendorScript = null;
let _seccoreCode = null;
let _mnsv2 = null;
let _b64Alphabet = null;  // 自定义 Base64 字母表
let _version = null;      // 版本号 (u.i8)

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? _https : _http;
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

// === 从 vendor-dynamic.js 提取自定义 Base64 字母表 ===
function extractB64Alphabet(vendorScript) {
  // 搜索 64 字符的自定义字母表
  // 在 base64 编码函数中，字母表通常紧跟在 for 循环或 charCodeAt 附近
  const re = /["']([A-Za-z0-9+/]{64})["']/g;
  let m;
  const candidates = [];
  while ((m = re.exec(vendorScript)) !== null) {
    const s = m[1];
    // 验证：64 个不重复字符
    if (new Set(s).size === 64) {
      // 排除标准 Base64 字母表
      if (s !== 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/') {
        candidates.push(s);
      }
    }
  }
  // 如果找到多个，优先选择已知的
  const known = 'ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5';
  for (const c of candidates) {
    if (c === known) return c;
  }
  return candidates[0] || null;
}

// === 从 vendor-dynamic.js 提取版本号 ===
function extractVersion(vendorScript) {
  // 搜索版本号模式：在 "xhs-pc-web" 附近的版本字符串
  // 通常格式为 X="数字.数字.数字" 在模块定义中
  const versionPatterns = [
    // 搜索 i8 导出附近的版本号
    /i8:\s*function\(\)\s*\{\s*return\s+(\w+)\b/,
    // 搜索 "xhs-pc-web" 附近的版本号
    /["'](\d+\.\d+\.\d+)["'][^}]*xhs-pc-web|xhs-pc-web[^}]*["'](\d+\.\d+\.\d+)["']/,
  ];

  // 方法1: 找 i8 导出
  const i8Match = vendorScript.match(/i8:\s*function\(\)\s*\{\s*return\s+(\w+)/);
  if (i8Match) {
    const varName = i8Match[1];
    // 在附近找这个变量的赋值
    const idx = i8Match.index;
    const nearby = vendorScript.substring(Math.max(0, idx - 5000), idx + 500);
    const verMatch = nearby.match(new RegExp(varName + '\\s*=\\s*["\']([\\d.]+)["\']'));
    if (verMatch) return verMatch[1];
  }

  // 方法2: 搜索常见版本号模式
  const allVersions = vendorScript.matchAll(/=\s*["'](\d+\.\d+\.\d+)["']/g);
  const candidates = [];
  for (const m of allVersions) {
    const v = m[1];
    if (v.match(/^\d+\.\d+\.\d+$/) && !v.startsWith('0.')) {
      candidates.push(v);
    }
  }
  // 返回出现频率最高的版本号（通常是主版本）
  if (candidates.length > 0) {
    const freq = {};
    for (const v of candidates) freq[v] = (freq[v] || 0) + 1;
    return Object.entries(freq).sort((a, b) => b[1] - a[1])[0][0];
  }

  return '3.8.7'; // 回退默认值
}

// === 自定义 Base64 编码 (h.xE) ===
function xhsB64Encode(byteArray) {
  const alphabet = _b64Alphabet || 'ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5';
  const len = byteArray.length;
  const remainder = len % 3;
  const chunks = [];

  // 编码每 3 字节为 4 个字符
  function encodeChunk(arr, start, end) {
    let tmp;
    const out = [];
    for (let i = start; i < end; i += 3) {
      tmp = ((arr[i] << 16) & 0xFF0000) + ((arr[i + 1] << 8) & 0xFF00) + (arr[i + 2] & 0xFF);
      out.push(
        alphabet[(tmp >> 18) & 0x3F] +
        alphabet[(tmp >> 12) & 0x3F] +
        alphabet[(tmp >> 6) & 0x3F] +
        alphabet[tmp & 0x3F]
      );
    }
    return out.join('');
  }

  const mainLen = len - remainder;
  for (let i = 0; i < mainLen; i += 16383) {
    chunks.push(encodeChunk(byteArray, i, i + 16383 > mainLen ? mainLen : i + 16383));
  }

  if (remainder === 1) {
    const a = byteArray[len - 1];
    chunks.push(alphabet[a >> 2] + alphabet[(a << 4) & 63] + '==');
  } else if (remainder === 2) {
    const a = (byteArray[len - 2] << 8) + byteArray[len - 1];
    chunks.push(alphabet[(a >> 10)] + alphabet[(a >> 4) & 63] + alphabet[(a << 2) & 63] + '=');
  }

  return chunks.join('');
}

// === UTF-8 编码 (h.lz) ===
function xhsUtf8Encode(str) {
  const encoded = encodeURIComponent(str);
  const result = [];
  for (let i = 0; i < encoded.length; i++) {
    const ch = encoded.charAt(i);
    if (ch === '%') {
      const hex = parseInt(encoded.charAt(i + 1) + encoded.charAt(i + 2), 16);
      result.push(hex);
      i += 2;
    } else {
      result.push(ch.charCodeAt(0));
    }
  }
  return result;
}

// === MD5 哈希 (h.Pu) ===
function xhsMd5(str) {
  return _nodeCrypto.createHash('md5').update(str).digest('hex');
}

// === CRC32 哈希 (h.tb) ===
const _crc32Table = (() => {
  const poly = 0xedb88320;
  const table = new Array(256);
  for (let i = 0; i < 256; i++) {
    let r = i;
    for (let j = 0; j < 8; j++) {
      r = (r & 1) ? (r >>> 1) ^ poly : r >>> 1;
    }
    table[i] = r >>> 0;
  }
  return table;
})();

function xhsCrc32(input) {
  let crc = -1;
  if (typeof input === 'string') {
    for (let i = 0; i < input.length; i++) {
      crc = _crc32Table[(crc ^ input.charCodeAt(i)) & 0xFF] ^ (crc >>> 8);
    }
  } else {
    for (let i = 0; i < input.length; i++) {
      crc = _crc32Table[(crc ^ input[i]) & 0xFF] ^ (crc >>> 8);
    }
  }
  return (-1 ^ crc ^ 0xedb88320) >>> 0;
}

// === 平台编码 (sw.SW) ===
function xhsPlatformCode(platform) {
  switch (platform) {
    case 'Android': return 2;
    case 'iOS': return 1;
    case 'Mac OS': return 3;
    case 'Linux': return 4;
    default: return 5; // "other" — 注意 Windows 不在 switch 中，走 default
  }
}

// === 构建完整 XYS_ 签名 ===
function buildXs(apiUrl, mnsResult) {
  const version = _version || '3.8.7';
  const payload = JSON.stringify({
    x0: version,
    x1: 'xhs-pc-web',
    x2: 'PC',
    x3: mnsResult,
    x4: ''
  });
  const utf8Bytes = xhsUtf8Encode(payload);
  return 'XYS_' + xhsB64Encode(utf8Bytes);
}

// === 构建 x-s-common ===
function buildXsc(xs, a1) {
  const version = _version || '3.8.7';
  const platform = 'PC';
  const b1 = '';
  const b1b1 = '1';
  const x7 = '';
  const sc = 0;
  const payload = JSON.stringify({
    s0: xhsPlatformCode(platform),
    s1: '',
    x0: b1b1,
    x1: version,
    x2: platform || 'PC',
    x3: 'xhs-pc-web',
    x4: '5.11.0',
    x5: a1,
    x6: xs,
    x7: x7,
    x8: b1,
    x9: xhsCrc32('' + xs + x7 + b1),
    x10: sc,
    x11: 'normal',
    x12: ''
  });
  const utf8Bytes = xhsUtf8Encode(payload);
  return xhsB64Encode(utf8Bytes);
}

function setupBrowserGlobals() {
  const chromeUA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36';

  // 覆盖 Node.js 22 内置的 navigator（它是 getter，需要 defineProperty）
  Object.defineProperty(globalThis, 'navigator', {
    value: {
      userAgent: chromeUA, platform: 'Win32', language: 'zh-CN', languages: ['zh-CN', 'zh'],
      hardwareConcurrency: 8, maxTouchPoints: 0, cookieEnabled: true, onLine: true,
      plugins: { length: 0 }, connection: { effectiveType: '4g', downlink: 10, rtt: 50 },
      webdriver: false, vendor: 'Google Inc.',
      appVersion: chromeUA.replace('Mozilla/', ''), product: 'Gecko', productSub: '20030107',
      appCodeName: 'Mozilla', appName: 'Netscape', mimeTypes: { length: 0 },
      doNotTrack: null, javaEnabled: () => false, sendBeacon: () => true,
    },
    writable: true, configurable: true, enumerable: true
  });

  // 隐藏 Node.js 特征
  const nodeGlobals = ['process', 'Buffer', 'require', 'module', 'exports', '__dirname', '__filename', 'global'];
  for (const name of nodeGlobals) {
    if (name in globalThis) {
      try { Object.defineProperty(globalThis, name, { value: undefined, writable: true, configurable: true }); }
      catch(e) { try { delete globalThis[name]; } catch(e2) {} }
    }
  }

  const perfStart = Date.now();
  globalThis.window = globalThis;
  globalThis.self = globalThis;
  globalThis.top = globalThis;

  globalThis.performance = {
    now: () => Date.now() - perfStart,
    timing: { navigationStart: perfStart - 5000 },
    getEntriesByType: () => [], mark: () => {}, measure: () => {},
  };

  // ★ 关键：crypto.getRandomValues — 没有这个 mnsv2 不会注册 ★
  globalThis.crypto = {
    getRandomValues: (arr) => {
      const bytes = _nodeCrypto.randomBytes(arr.byteLength);
      const view = new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength);
      for (let i = 0; i < view.length; i++) view[i] = bytes[i];
      return arr;
    },
    subtle: {
      digest: async (algo, data) => {
        const name = algo.replace('-', '').toLowerCase();
        const hash = _nodeCrypto.createHash(name === 'sha256' ? 'sha256' : name === 'sha1' ? 'sha1' : 'md5');
        hash.update(new Uint8Array(data));
        const r = hash.digest();
        return r.buffer.slice(r.byteOffset, r.byteOffset + r.byteLength);
      },
    },
    randomUUID: () => _nodeCrypto.randomUUID(),
  };

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
          toDataURL: () => 'data:image/png;base64,iVBOR', width: 300, height: 150,
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
    cookie: '', title: '', referrer: 'https://www.xiaohongshu.com/',
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
  globalThis.MutationObserver = class { constructor() {} observe() {} disconnect() {} };
  globalThis.IntersectionObserver = class { constructor() {} observe() {} disconnect() {} };
  globalThis.ResizeObserver = class { constructor() {} observe() {} disconnect() {} };
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
  globalThis.Blob = class { constructor(p, o) { this.size = 0; this.type = o?.type || ''; } };
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
    ok: true, status: 200, text: () => Promise.resolve(''),
    json: () => Promise.resolve({}), headers: { get: () => null },
  });
}

async function initSeccore() {
  if (_mnsv2) return _mnsv2;

  _console.error('[seccore] 下载 vendor-dynamic.js...');
  if (!_vendorScript) _vendorScript = await fetchUrl(VENDOR_URL);
  _console.error(`[seccore] vendor-dynamic.js 大小: ${_vendorScript.length}`);

  _console.error('[seccore] 提取 seccore 代码...');
  if (!_seccoreCode) _seccoreCode = extractSeccoreCode(_vendorScript);
  if (!_seccoreCode) {
    _console.error('[seccore] 提取失败');
    return null;
  }
  _console.error(`[seccore] 代码长度: ${_seccoreCode.length}`);

  // 提取自定义 Base64 字母表和版本号
  if (!_b64Alphabet) {
    _b64Alphabet = extractB64Alphabet(_vendorScript);
    _console.error(`[seccore] Base64 字母表: ${_b64Alphabet ? _b64Alphabet.substring(0, 20) + '...' : '未找到，使用默认'}`);
  }
  if (!_version) {
    _version = extractVersion(_vendorScript);
    _console.error(`[seccore] 版本号: ${_version}`);
  }

  // 设置浏览器环境（修改 globalThis）
  setupBrowserGlobals();

  // 在全局作用域中执行 seccore 代码
  _console.error('[seccore] 执行 seccore 代码...');
  try {
    const fn = new Function(_seccoreCode);
    fn();
  } catch (e) {
    _console.error(`[seccore] 执行错误: ${e.message}`);
    return null;
  }

  if (typeof globalThis.mnsv2 === 'function') {
    _console.error('[seccore] mnsv2 注册成功');
    _mnsv2 = globalThis.mnsv2;
    return _mnsv2;
  }

  // 等待异步注册
  _console.error('[seccore] 等待 mnsv2 异步注册...');
  for (let i = 0; i < 20; i++) {
    await new Promise(r => _setTimeout(r, 500));
    if (typeof globalThis.mnsv2 === 'function') {
      _console.error(`[seccore] mnsv2 在 ${(i+1)*0.5}s 后注册成功`);
      _mnsv2 = globalThis.mnsv2;
      return _mnsv2;
    }
  }

  _console.error('[seccore] mnsv2 注册失败');
  return null;
}

// === HTTP 服务模式 ===
async function startServer(port) {
  const mnsv2 = await initSeccore();
  if (!mnsv2) {
    _console.error('[seccore] 初始化失败');
    _process.exit(1);
  }

  // 测试签名
  try {
    const testUrl = '/api/sns/web/v2/comment/page?note_id=test';
    const md5 = xhsMd5(testUrl);
    const sig = mnsv2(testUrl, md5);
    _console.error(`[seccore] 测试签名: ${String(sig).substring(0, 60)}... (长度: ${String(sig).length})`);
    const testXs = buildXs(testUrl, sig);
    _console.error(`[seccore] 测试 XYS_: ${testXs.substring(0, 60)}...`);
  } catch (e) {
    _console.error(`[seccore] 测试签名失败: ${e.message}`);
  }

  // 恢复 Node.js 全局对象（HTTP 服务需要）
  globalThis.process = _process;
  globalThis.Buffer = _Buffer;
  globalThis.require = _require;

  const server = _http.createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${port}`);

    if (url.pathname === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, type: 'seccore_mnsv2' }));
      return;
    }

    if (url.pathname === '/sign') {
      const apiUrl = url.searchParams.get('url');
      const a1 = url.searchParams.get('a1') || '';
      if (!apiUrl) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'missing url param' }));
        return;
      }
      try {
        // 使用正确的 webpack 辅助函数构建签名
        const md5Hash = xhsMd5(apiUrl);
        const mns = mnsv2(apiUrl, md5Hash);  // 2 参数调用
        const xt = String(Date.now());
        const xs = buildXs(apiUrl, mns);
        const xsc = buildXsc(xs, a1);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ xs, xt, xsc, mns, md5: md5Hash }));
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
      return;
    }

    res.writeHead(404);
    res.end('Not Found');
  });

  server.listen(port, () => {
    _console.error(`[seccore] 签名服务已启动: http://127.0.0.1:${port}`);
    _console.error(`[seccore] 用法: GET /sign?url=/api/sns/web/v2/...`);
  });
}

// === 单次调用模式 ===
async function signOnce(apiUrl) {
  const mnsv2 = await initSeccore();
  if (!mnsv2) {
    _process.stdout.write(JSON.stringify({ error: 'seccore init failed' }));
    _process.exit(1);
  }
  try {
    const md5Hash = xhsMd5(apiUrl);
    const mns = mnsv2(apiUrl, md5Hash);  // 2 参数调用
    const xt = String(Date.now());
    const xs = buildXs(apiUrl, mns);
    const xsc = buildXsc(xs, '');
    _process.stdout.write(JSON.stringify({ xs, xt, xsc, mns, md5: md5Hash }));
  } catch (e) {
    _process.stdout.write(JSON.stringify({ error: e.message }));
    _process.exit(1);
  }
}

// === 入口 ===
const args = _process.argv.slice(2);
if (args[0] === '--server') {
  const port = parseInt(args[1]) || 5679;
  startServer(port);
} else if (args[0]) {
  signOnce(args[0]);
} else {
  _console.log('用法:');
  _console.log('  node seccore_sign.js --server 5679     # HTTP 服务模式');
  _console.log('  node seccore_sign.js "/api/..."         # 单次调用');
}
