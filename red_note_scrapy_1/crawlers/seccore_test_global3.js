/**
 * 测试3：添加 crypto.getRandomValues 和其他可能缺失的 Web API
 *
 * 假设：字节码 VM 内部使用了 crypto.getRandomValues 生成随机数，
 * 这是浏览器特有的 API，Node.js 全局没有（Node.js 的 crypto 是不同的模块）
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
  const _Buffer = Buffer;
  const _process = process;

  _console.error('[test3] 下载 vendor-dynamic.js...');
  const vendorScript = await fetchUrl(VENDOR_URL);
  _console.error(`[test3] 大小: ${vendorScript.length}`);

  const code = extractSeccoreCode(vendorScript);
  if (!code) { _console.error('[test3] 提取失败'); _process.exit(1); }
  _console.error(`[test3] 代码长度: ${code.length}`);

  // === 隐藏 Node.js 特征 ===
  const chromeUA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36';

  Object.defineProperty(globalThis, 'navigator', {
    value: {
      userAgent: chromeUA,
      platform: 'Win32', language: 'zh-CN', languages: ['zh-CN', 'zh'],
      hardwareConcurrency: 8, maxTouchPoints: 0,
      cookieEnabled: true, onLine: true,
      plugins: { length: 0, 0: { name: 'PDF Viewer', filename: 'internal-pdf-viewer' } },
      connection: { effectiveType: '4g', downlink: 10, rtt: 50 },
      webdriver: false,
      vendor: 'Google Inc.',
      appVersion: chromeUA.replace('Mozilla/', ''),
      product: 'Gecko', productSub: '20030107',
      appCodeName: 'Mozilla', appName: 'Netscape',
      mimeTypes: { length: 0 },
      doNotTrack: null,
      getBattery: () => Promise.resolve({ charging: true, chargingTime: 0, dischargingTime: Infinity, level: 1 }),
      getGamepads: () => [],
      javaEnabled: () => false,
      sendBeacon: () => true,
      vibrate: () => true,
    },
    writable: true, configurable: true, enumerable: true
  });

  // 隐藏 Node.js 全局对象
  const nodeGlobals = ['process', 'Buffer', 'require', 'module', 'exports', '__dirname', '__filename', 'global'];
  const saved = {};
  for (const name of nodeGlobals) {
    if (name in globalThis) {
      saved[name] = globalThis[name];
      try {
        Object.defineProperty(globalThis, name, { value: undefined, writable: true, configurable: true });
      } catch(e) { try { delete globalThis[name]; } catch(e2) {} }
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
    getEntriesByType: () => [],
    mark: () => {}, measure: () => {},
  };

  // ★★★ 关键：crypto.getRandomValues ★★★
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
      importKey: async () => ({}),
      exportKey: async () => new ArrayBuffer(0),
      encrypt: async () => new ArrayBuffer(0),
      decrypt: async () => new ArrayBuffer(0),
    },
    randomUUID: () => nodeCrypto.randomUUID(),
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
          toDataURL: () => 'data:image/png;base64,iVBOR',
          width: 300, height: 150,
        };
      }
      if (tag === 'div' || tag === 'span' || tag === 'p') {
        return {
          style: {}, appendChild: () => {}, setAttribute: () => {},
          addEventListener: () => {}, removeEventListener: () => {},
          innerHTML: '', textContent: '', offsetHeight: 0, offsetWidth: 0,
          getBoundingClientRect: () => ({ top: 0, left: 0, bottom: 0, right: 0, width: 0, height: 0 }),
        };
      }
      return {
        style: {}, appendChild: () => {}, setAttribute: () => {},
        addEventListener: () => {}, removeEventListener: () => {},
        innerHTML: '', textContent: '',
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
    readyState: 'complete',
    visibilityState: 'visible',
    hidden: false,
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
  globalThis.MutationObserver = class { constructor(cb) { this._cb = cb; } observe() {} disconnect() {} takeRecords() { return []; } };
  globalThis.IntersectionObserver = class { constructor(cb) {} observe() {} disconnect() {} };
  globalThis.ResizeObserver = class { constructor(cb) {} observe() {} disconnect() {} };
  globalThis.Image = class { constructor() { this.onload = null; this.onerror = null; } set src(v) { if (this.onload) _setTimeout(() => this.onload(), 0); } };
  globalThis.Event = class Event { constructor(type) { this.type = type; } };
  globalThis.CustomEvent = class CustomEvent extends globalThis.Event { constructor(type, opts) { super(type); this.detail = opts?.detail; } };
  globalThis.MessageEvent = class extends globalThis.Event {};
  globalThis.history = { pushState: () => {}, replaceState: () => {}, back: () => {}, forward: () => {}, go: () => {} };
  globalThis.requestAnimationFrame = (cb) => _setTimeout(cb, 16);
  globalThis.cancelAnimationFrame = (id) => _clearTimeout(id);
  globalThis.requestIdleCallback = (cb) => _setTimeout(() => cb({ didTimeout: false, timeRemaining: () => 50 }), 0);
  globalThis.getComputedStyle = () => new Proxy({}, { get: () => '' });
  globalThis.matchMedia = () => ({ matches: false, addListener: () => {}, removeListener: () => {}, addEventListener: () => {} });
  globalThis.btoa = (s) => _Buffer.from(s, 'binary').toString('base64');
  globalThis.atob = (s) => _Buffer.from(s, 'base64').toString('binary');
  globalThis.InstallTrigger = undefined;
  globalThis.Blob = class Blob { constructor(parts, opts) { this.size = 0; this.type = opts?.type || ''; } };
  globalThis.URL = class URL { constructor(url, base) { this.href = url; } static createObjectURL() { return 'blob:null'; } static revokeObjectURL() {} };
  globalThis.Worker = class { constructor() {} postMessage() {} terminate() {} };
  globalThis.MessageChannel = class { constructor() { this.port1 = { onmessage: null, postMessage: () => {} }; this.port2 = { onmessage: null, postMessage: () => {} }; } };
  globalThis.AbortController = class { constructor() { this.signal = { aborted: false, addEventListener: () => {} }; } abort() { this.signal.aborted = true; } };
  globalThis.DOMParser = class { parseFromString() { return globalThis.document; } };

  // XMLHttpRequest
  globalThis.XMLHttpRequest = class {
    constructor() {
      this.readyState = 0; this.status = 0; this.responseText = ''; this.response = '';
      this.onreadystatechange = null; this.onload = null; this.onerror = null;
      this._headers = {};
    }
    open(method, url) { this._method = method; this._url = url; this.readyState = 1; }
    setRequestHeader(k, v) { this._headers[k] = v; }
    getResponseHeader() { return null; }
    getAllResponseHeaders() { return ''; }
    send(body) {
      _console.error(`[xhr] ${this._method} ${String(this._url).substring(0, 120)}`);
      if (body) _console.error(`[xhr:body] ${String(body).substring(0, 500)}`);
      this.status = 200; this.responseText = '{}'; this.response = '{}'; this.readyState = 4;
      const self = this;
      if (this.onreadystatechange) _setTimeout(() => self.onreadystatechange(), 0);
      if (this.onload) _setTimeout(() => self.onload(), 0);
    }
    abort() {}
  };

  // fetch mock
  globalThis.fetch = (url, opts) => {
    _console.error(`[fetch] ${opts?.method || 'GET'} ${String(url).substring(0, 120)}`);
    return Promise.resolve({
      ok: true, status: 200, statusText: 'OK',
      text: () => Promise.resolve('{}'),
      json: () => Promise.resolve({}),
      headers: { get: () => null },
    });
  };

  // === 验证 ===
  _console.error(`[test3] navigator.userAgent: ${globalThis.navigator.userAgent}`);
  _console.error(`[test3] typeof crypto: ${typeof globalThis.crypto}`);
  _console.error(`[test3] typeof crypto.getRandomValues: ${typeof globalThis.crypto.getRandomValues}`);
  _console.error(`[test3] typeof process: ${typeof globalThis.process}`);

  // 测试 crypto.getRandomValues
  const testArr = new Uint8Array(4);
  globalThis.crypto.getRandomValues(testArr);
  _console.error(`[test3] crypto.getRandomValues 测试: [${testArr.join(',')}]`);

  // === 执行 ===
  _console.error('[test3] 执行 seccore 代码...');
  try {
    const fn = new Function(code);
    fn();
  } catch (e) {
    _console.error(`[test3] 执行错误: ${e.message}`);
    _console.error(e.stack);
  }

  _console.error(`[test3] mnsv2: ${typeof globalThis.mnsv2}`);

  if (typeof globalThis.mnsv2 === 'function') {
    _console.error('[test3] 成功!');
    try {
      const result = globalThis.mnsv2('/api/test', 'abc', 'def');
      _console.error(`[test3] 签名: ${String(result).substring(0, 80)}... (长度: ${String(result).length})`);
    } catch (e) {
      _console.error(`[test3] 调用失败: ${e.message}`);
    }
    _process.exit(0);
    return;
  }

  _console.error('[test3] 等待异步...');
  for (let i = 0; i < 15; i++) {
    await new Promise(r => _setTimeout(r, 1000));
    if (typeof globalThis.mnsv2 === 'function') {
      _console.error(`[test3] mnsv2 在 ${i+1}s 后注册!`);
      try {
        const result = globalThis.mnsv2('/api/test', 'abc', 'def');
        _console.error(`[test3] 签名: ${String(result).substring(0, 80)}... (长度: ${String(result).length})`);
      } catch (e) {
        _console.error(`[test3] 调用失败: ${e.message}`);
      }
      break;
    }
    if (i % 3 === 2) _console.error(`[test3] 等待中... (${i+1}s)`);
  }

  if (typeof globalThis.mnsv2 !== 'function') {
    _console.error('[test3] 失败');
    const fns = Object.keys(globalThis).filter(k => {
      try { return typeof globalThis[k] === 'function' && k.startsWith('_') && k.length > 10; } catch(e) { return false; }
    });
    _console.error(`[test3] 全局函数(${fns.length}): ${fns.join(', ')}`);
  }

  for (const [name, val] of Object.entries(saved)) globalThis[name] = val;
  process.exit(0);
})();
