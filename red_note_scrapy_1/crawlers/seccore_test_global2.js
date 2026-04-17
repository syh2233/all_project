/**
 * 测试2：彻底隐藏 Node.js 环境特征
 *
 * 发现：字节码通过 navigator.userAgent 检测到 "Node.js/22"
 * 说明我们的 navigator mock 没有生效，或者字节码通过其他方式检测
 *
 * 方案：
 * 1. 删除 process, require, module, exports, __dirname, __filename 等 Node.js 特征
 * 2. 用 Object.defineProperty 覆盖 navigator（Node.js 22 内置 navigator 可能是不可写的）
 * 3. 隐藏 Buffer, global 等 Node.js 特有对象
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
  try {
    return JSON.parse('"' + rawInSource + '"');
  } catch (e) {
    return null;
  }
}

(async () => {
  console.error('[test2] 下载 vendor-dynamic.js...');
  const vendorScript = await fetchUrl(VENDOR_URL);
  console.error(`[test2] 大小: ${vendorScript.length}`);

  const code = extractSeccoreCode(vendorScript);
  if (!code) { console.error('[test2] 提取失败'); process.exit(1); }
  console.error(`[test2] 代码长度: ${code.length}`);

  // === 第一步：检查 Node.js 22 的 navigator 是否可写 ===
  console.error(`[test2] 原始 navigator.userAgent: ${typeof navigator !== 'undefined' ? navigator.userAgent : 'undefined'}`);
  const navDesc = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  console.error(`[test2] navigator 描述符: ${JSON.stringify({
    writable: navDesc?.writable,
    configurable: navDesc?.configurable,
    enumerable: navDesc?.enumerable,
    hasGet: !!navDesc?.get,
    hasSet: !!navDesc?.set,
  })}`);

  // === 第二步：检查 process 是否可删除 ===
  const procDesc = Object.getOwnPropertyDescriptor(globalThis, 'process');
  console.error(`[test2] process 描述符: ${JSON.stringify({
    writable: procDesc?.writable,
    configurable: procDesc?.configurable,
    enumerable: procDesc?.enumerable,
  })}`);

  // === 第三步：保存需要的 Node.js 引用 ===
  const _setTimeout = setTimeout;
  const _clearTimeout = clearTimeout;
  const _setInterval = setInterval;
  const _clearInterval = clearInterval;
  const _process = process;
  const _Buffer = Buffer;
  const _require = require;
  const _console = console;

  // === 第四步：用 Object.defineProperty 强制覆盖 navigator ===
  const chromeUA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36';
  const fakeNavigator = {
    userAgent: chromeUA,
    platform: 'Win32', language: 'zh-CN', languages: ['zh-CN', 'zh'],
    hardwareConcurrency: 8, maxTouchPoints: 0,
    cookieEnabled: true, onLine: true,
    plugins: { length: 0 },
    connection: { effectiveType: '4g', downlink: 10, rtt: 50 },
    webdriver: false,
    vendor: 'Google Inc.',
    appVersion: chromeUA.replace('Mozilla/', ''),
    product: 'Gecko',
    productSub: '20030107',
    appCodeName: 'Mozilla',
    appName: 'Netscape',
  };

  try {
    Object.defineProperty(globalThis, 'navigator', {
      value: fakeNavigator, writable: true, configurable: true, enumerable: true
    });
  } catch(e) {
    _console.error(`[test2] 覆盖 navigator 失败: ${e.message}`);
    // 尝试删除后重新定义
    try {
      delete globalThis.navigator;
      globalThis.navigator = fakeNavigator;
    } catch(e2) {
      _console.error(`[test2] 删除+重设 navigator 也失败: ${e2.message}`);
    }
  }
  _console.error(`[test2] 覆盖后 navigator.userAgent: ${globalThis.navigator.userAgent}`);

  // === 第五步：隐藏 Node.js 特征 ===
  // 保存 process.exit 引用
  const _exit = _process.exit.bind(_process);

  // 隐藏 Node.js 特有全局对象
  const nodeGlobals = ['process', 'Buffer', 'require', 'module', 'exports', '__dirname', '__filename', 'global'];
  const savedNodeGlobals = {};
  for (const name of nodeGlobals) {
    if (name in globalThis) {
      savedNodeGlobals[name] = globalThis[name];
      try {
        Object.defineProperty(globalThis, name, {
          value: undefined, writable: true, configurable: true
        });
      } catch(e) {
        try { delete globalThis[name]; } catch(e2) {}
      }
    }
  }

  // === 第六步：设置浏览器环境 ===
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
    };
  };
  globalThis.localStorage = createStorage();
  globalThis.sessionStorage = createStorage();
  globalThis.screen = { width: 1920, height: 1080, availWidth: 1920, availHeight: 1040, colorDepth: 24, pixelDepth: 24 };
  globalThis.chrome = { runtime: {}, webstore: {} };
  globalThis.MutationObserver = class { constructor() {} observe() {} disconnect() {} };
  globalThis.Image = class { set src(v) {} };
  globalThis.Event = class {};
  globalThis.CustomEvent = class extends globalThis.Event {};
  globalThis.history = { pushState: () => {}, replaceState: () => {} };
  globalThis.requestAnimationFrame = (cb) => _setTimeout(cb, 16);
  globalThis.cancelAnimationFrame = (id) => _clearTimeout(id);
  globalThis.getComputedStyle = () => ({});
  globalThis.matchMedia = () => ({ matches: false, addListener: () => {} });
  globalThis.btoa = (s) => _Buffer.from(s, 'binary').toString('base64');
  globalThis.atob = (s) => _Buffer.from(s, 'base64').toString('binary');
  globalThis.InstallTrigger = undefined;

  // XMLHttpRequest mock
  globalThis.XMLHttpRequest = class {
    constructor() {
      this.readyState = 0; this.status = 0; this.responseText = '';
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
      this.status = 200; this.responseText = '{}'; this.readyState = 4;
      const self = this;
      if (this.onreadystatechange) _setTimeout(() => self.onreadystatechange(), 0);
      if (this.onload) _setTimeout(() => self.onload(), 0);
    }
    abort() {}
  };

  // === 第七步：验证环境 ===
  _console.error(`[test2] 验证: navigator.userAgent = ${globalThis.navigator.userAgent}`);
  _console.error(`[test2] 验证: typeof process = ${typeof globalThis.process}`);
  _console.error(`[test2] 验证: typeof require = ${typeof globalThis.require}`);
  _console.error(`[test2] 验证: typeof Buffer = ${typeof globalThis.Buffer}`);
  _console.error(`[test2] 验证: typeof module = ${typeof globalThis.module}`);
  _console.error(`[test2] 验证: typeof window = ${typeof globalThis.window}`);
  _console.error(`[test2] 验证: typeof document = ${typeof globalThis.document}`);

  // === 第八步：执行 seccore 代码 ===
  _console.error('[test2] 执行 seccore 代码...');
  try {
    const fn = new Function(code);
    fn();
  } catch (e) {
    _console.error(`[test2] 执行错误: ${e.message}`);
    _console.error(e.stack);
  }

  // === 第九步：检查结果 ===
  _console.error(`[test2] mnsv2 类型: ${typeof globalThis.mnsv2}`);
  _console.error(`[test2] _AUuXfEG27Xa3x 类型: ${typeof globalThis._AUuXfEG27Xa3x}`);

  if (typeof globalThis.mnsv2 === 'function') {
    _console.error('[test2] mnsv2 立即注册成功!');
    try {
      const result = globalThis.mnsv2('/api/test', 'abc', 'def');
      _console.error(`[test2] 签名: ${String(result).substring(0, 80)}... (长度: ${String(result).length})`);
    } catch (e) {
      _console.error(`[test2] 调用失败: ${e.message}`);
    }
    _exit(0);
    return;
  }

  _console.error('[test2] mnsv2 未立即注册，等待异步...');

  // 恢复 process 以便 setTimeout 正常工作
  // (setTimeout 已经保存了引用，不需要恢复)

  for (let i = 0; i < 15; i++) {
    await new Promise(r => _setTimeout(r, 1000));
    if (typeof globalThis.mnsv2 === 'function') {
      _console.error(`[test2] mnsv2 在 ${i+1}s 后注册成功!`);
      try {
        const result = globalThis.mnsv2('/api/test', 'abc', 'def');
        _console.error(`[test2] 签名: ${String(result).substring(0, 80)}... (长度: ${String(result).length})`);
      } catch (e) {
        _console.error(`[test2] 调用失败: ${e.message}`);
      }
      break;
    }
    if (i % 3 === 2) _console.error(`[test2] 等待中... (${i+1}s)`);
  }

  if (typeof globalThis.mnsv2 !== 'function') {
    _console.error('[test2] mnsv2 注册失败');
    const newFuncs = Object.keys(globalThis).filter(k => {
      try { return typeof globalThis[k] === 'function' && k.startsWith('_') && k.length > 10; } catch(e) { return false; }
    });
    _console.error(`[test2] 全局函数: ${newFuncs.join(', ')}`);
  }

  // 恢复 Node.js 全局对象
  for (const [name, val] of Object.entries(savedNodeGlobals)) {
    globalThis[name] = val;
  }

  process.exit(0);
})();
