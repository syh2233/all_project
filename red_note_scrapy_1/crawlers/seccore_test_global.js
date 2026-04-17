/**
 * 测试：在 Node.js 全局作用域中执行 seccore 代码（不使用 vm 沙箱）
 *
 * 假设：vm 沙箱中的 Function 构造器行为与浏览器不同，
 * 导致字节码 VM 内部的 new Function() 调用失败。
 *
 * 方案：直接修改 globalThis，在全局作用域中执行 seccore 代码。
 */

const https = require('https');
const crypto = require('crypto');

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

  const rawInSource = vendorScript.substring(rawStart, rawEnd);
  let code;
  try {
    code = JSON.parse('"' + rawInSource + '"');
  } catch (e) {
    return null;
  }
  return code;
}

// === 在全局作用域中模拟浏览器环境 ===
function setupGlobalBrowserEnv() {
  const perfStart = Date.now();

  // 保存原始值以便恢复
  const originals = {};

  function setGlobal(name, value) {
    originals[name] = globalThis[name];
    globalThis[name] = value;
  }

  setGlobal('window', globalThis);
  setGlobal('self', globalThis);

  setGlobal('performance', {
    now: () => Date.now() - perfStart,
    timing: { navigationStart: perfStart - 5000 },
    getEntriesByType: () => [],
    mark: () => {}, measure: () => {},
  });

  setGlobal('document', {
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
        innerHTML: '', textContent: '',
      };
    },
    addEventListener: () => {}, removeEventListener: () => {},
    getElementById: () => null, querySelector: () => null,
    querySelectorAll: () => [], getElementsByTagName: () => [],
    cookie: '', title: '', referrer: 'https://www.xiaohongshu.com/',
    documentElement: { style: {} },
    body: { appendChild: () => {}, removeChild: () => {} },
    head: { appendChild: () => {} },
    location: { href: 'https://www.xiaohongshu.com/', hostname: 'www.xiaohongshu.com', protocol: 'https:' },
  });

  setGlobal('navigator', {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    platform: 'Win32', language: 'zh-CN', languages: ['zh-CN', 'zh'],
    hardwareConcurrency: 8, maxTouchPoints: 0,
    cookieEnabled: true, onLine: true,
    plugins: { length: 0 },
    connection: { effectiveType: '4g', downlink: 10, rtt: 50 },
    webdriver: false,
  });

  setGlobal('location', globalThis.document.location);

  const createStorage = () => {
    const store = {};
    return {
      getItem: (k) => store[k] || null,
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: (k) => { delete store[k]; },
      clear: () => { for (const k in store) delete store[k]; },
      get length() { return Object.keys(store).length; },
    };
  };
  setGlobal('localStorage', createStorage());
  setGlobal('sessionStorage', createStorage());

  setGlobal('screen', { width: 1920, height: 1080, availWidth: 1920, availHeight: 1040, colorDepth: 24, pixelDepth: 24 });

  return originals;
}

(async () => {
  console.error('[test] 下载 vendor-dynamic.js...');
  const vendorScript = await fetchUrl(VENDOR_URL);
  console.error(`[test] 大小: ${vendorScript.length}`);

  console.error('[test] 提取 seccore 代码...');
  const code = extractSeccoreCode(vendorScript);
  if (!code) {
    console.error('[test] 提取失败');
    process.exit(1);
  }
  console.error(`[test] 代码长度: ${code.length}`);

  // 设置全局浏览器环境
  const originals = setupGlobalBrowserEnv();

  // 添加更多全局对象
  globalThis.chrome = { runtime: {}, webstore: {} };
  globalThis.top = globalThis;
  globalThis.MutationObserver = class { constructor() {} observe() {} disconnect() {} };
  globalThis.Image = class { set src(v) {} };
  globalThis.Event = class {};
  globalThis.CustomEvent = class extends globalThis.Event {};
  globalThis.history = { pushState: () => {}, replaceState: () => {} };
  globalThis.requestAnimationFrame = (cb) => setTimeout(cb, 16);
  globalThis.cancelAnimationFrame = (id) => clearTimeout(id);
  globalThis.getComputedStyle = () => ({});
  globalThis.matchMedia = () => ({ matches: false, addListener: () => {} });
  globalThis.btoa = (s) => Buffer.from(s, 'binary').toString('base64');
  globalThis.atob = (s) => Buffer.from(s, 'base64').toString('binary');
  globalThis.InstallTrigger = undefined;

  // XMLHttpRequest mock（只记录，不真正发请求）
  globalThis.XMLHttpRequest = class {
    constructor() {
      this.readyState = 0; this.status = 0; this.responseText = '';
      this.onreadystatechange = null; this.onload = null; this.onerror = null;
      this._headers = {};
    }
    open(method, url) {
      this._method = method; this._url = url; this.readyState = 1;
    }
    setRequestHeader(k, v) { this._headers[k] = v; }
    getResponseHeader() { return null; }
    getAllResponseHeaders() { return ''; }
    send(body) {
      console.error(`[xhr] ${this._method} ${String(this._url).substring(0, 120)}`);
      if (body) console.error(`[xhr:body] ${String(body).substring(0, 500)}`);
      // 模拟成功响应
      this.status = 200; this.responseText = '{}'; this.readyState = 4;
      if (this.onreadystatechange) setTimeout(() => this.onreadystatechange(), 0);
      if (this.onload) setTimeout(() => this.onload(), 0);
    }
    abort() {}
  };

  console.error('[test] 在全局作用域中执行 seccore 代码...');
  try {
    // 关键区别：使用 new Function() 在全局作用域中执行，而不是 vm.runInContext
    const fn = new Function(code);
    fn();
  } catch (e) {
    console.error(`[test] 执行错误: ${e.message}`);
    console.error(e.stack);
  }

  // 检查 mnsv2
  console.error(`[test] mnsv2 类型: ${typeof globalThis.mnsv2}`);
  console.error(`[test] _AUuXfEG27Xa3x 类型: ${typeof globalThis._AUuXfEG27Xa3x}`);

  if (typeof globalThis.mnsv2 === 'function') {
    console.error('[test] mnsv2 立即注册成功!');
    try {
      const result = globalThis.mnsv2('/api/test', 'abc', 'def');
      console.error(`[test] 签名结果: ${String(result).substring(0, 80)}... (长度: ${String(result).length})`);
    } catch (e) {
      console.error(`[test] 调用 mnsv2 失败: ${e.message}`);
    }
  } else {
    console.error('[test] mnsv2 未立即注册，等待异步...');
    for (let i = 0; i < 10; i++) {
      await new Promise(r => setTimeout(r, 1000));
      if (typeof globalThis.mnsv2 === 'function') {
        console.error(`[test] mnsv2 在 ${i+1}s 后注册成功!`);
        try {
          const result = globalThis.mnsv2('/api/test', 'abc', 'def');
          console.error(`[test] 签名结果: ${String(result).substring(0, 80)}... (长度: ${String(result).length})`);
        } catch (e) {
          console.error(`[test] 调用 mnsv2 失败: ${e.message}`);
        }
        break;
      }
      if (i % 2 === 1) console.error(`[test] 等待中... (${i+1}s)`);
    }

    if (typeof globalThis.mnsv2 !== 'function') {
      console.error('[test] mnsv2 注册失败');
      // 列出新注册的全局函数
      const newFuncs = Object.keys(globalThis).filter(k => {
        try { return typeof globalThis[k] === 'function' && k.startsWith('_') && k.length > 10; } catch(e) { return false; }
      });
      console.error(`[test] 全局函数: ${newFuncs.join(', ')}`);
    }
  }

  process.exit(0);
})();
