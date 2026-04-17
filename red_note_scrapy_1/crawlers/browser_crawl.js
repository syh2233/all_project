/**
 * 浏览器内评论爬虫脚本
 *
 * 使用方法：
 * 1. 在浏览器中打开小红书笔记页面
 * 2. 打开 DevTools Console
 * 3. 粘贴此脚本执行
 * 4. 等待爬取完成后，结果保存在 window._crawlResult
 * 5. 在 Console 中执行 copy(JSON.stringify(window._crawlResult)) 复制到剪贴板
 */

(async function() {
  'use strict';

  // ===== 配置 =====
  const NOTE_ID = '699dd0b1000000001d024fe6';
  const INIT_TOKEN = 'ABsRvLIMkL008_96o22gryTaZWQ1hS6ndztRDFWXI1M5s=';
  const REQUEST_DELAY = [8000, 15000];   // 每次请求间隔 (ms)
  const RETRY_DELAY = [60000, 90000];    // 461 重试延迟 (ms)
  const COOLDOWN_DELAY = [60000, 90000]; // 主动冷却延迟 (ms)
  const MAX_RETRIES = 5;
  const REQUESTS_BEFORE_COOLDOWN = 10;   // 每N次请求后主动休息

  // ===== 请求计数器 =====
  let requestCount = 0;

  // ===== 初始化签名模块 =====
  let wr;
  window.webpackChunkxhs_pc_web.push([['_crawl_'], {}, (r) => { wr = r; }]);
  const h = wr(69431);   // Pu, xE, lz, tb
  const m = wr(31547);   // _ (typeof)
  const u = wr(55340);   // constants
  const sw = wr(4301);   // SW function

  function signUrl(url, data) {
    let f = url;
    const a = window.toString;
    if ("[object Object]" === a.call(data) || "[object Array]" === a.call(data) ||
        (void 0 === data ? "undefined" : m._(data)) === "object" && null !== data) {
      f += JSON.stringify(data);
    } else if ("string" === typeof data) { f += data; }
    const c = h.Pu([f].join("")), d = h.Pu(url);
    const s = window.mnsv2(f, c, d);
    const payload = { x0: u.i8, x1: "xhs-pc-web", x2: window[u.mj] || "PC", x3: s, x4: data ? (void 0 === data ? "undefined" : m._(data)) : "" };
    return { xs: "XYS_" + h.xE(h.lz(JSON.stringify(payload))), xt: String(Date.now()) };
  }

  function buildXsCommon(url, xs) {
    const platform = window[u.mj] || "PC";
    const a1 = (document.cookie.match(/a1=([^;]+)/) || [])[1] || "";
    const b1 = localStorage.getItem('b1') || '';
    const b1b1 = localStorage.getItem('b1b1') || '1';
    const sc = Number(sessionStorage.getItem('sc')) || 0;
    sessionStorage.setItem('sc', String(sc + 1));
    const dsl = window._dsl || '', x6 = xs, x7 = dsl ? ";" + dsl : "";
    const y = { s0: sw.SW(platform), s1: "", x0: b1b1, x1: u.i8, x2: platform || "PC", x3: "xhs-pc-web", x4: "5.11.0", x5: a1, x6, x7, x8: b1, x9: Number(h.tb("" + x6 + x7 + b1)), x10: sc, x11: "normal", x12: localStorage.getItem('b1c1') || "" };
    return h.xE(h.lz(JSON.stringify(y)));
  }

  function sleep(min, max) {
    const ms = min + Math.random() * (max - min);
    return new Promise(r => setTimeout(r, ms));
  }

  async function apiGet(path) {
    // 主动冷却：每N次请求后休息
    requestCount++;
    if (requestCount % REQUESTS_BEFORE_COOLDOWN === 0) {
      console.log(`  ⏸️ 已发${requestCount}次请求，主动冷却60-90秒...`);
      await sleep(...COOLDOWN_DELAY);
    }

    for (let i = 0; i < MAX_RETRIES; i++) {
      const { xs, xt } = signUrl(path);
      const xsc = buildXsCommon(path, xs);
      const resp = await fetch('https://edith.xiaohongshu.com' + path, {
        method: 'GET',
        headers: { 'accept': 'application/json, text/plain, */*', 'x-s': xs, 'x-t': xt, 'x-s-common': xsc },
        credentials: 'include'
      });
      if (resp.status === 200) return resp.json();
      if (resp.status === 461 && i < MAX_RETRIES - 1) {
        console.log(`  ⚠️ 461 频率限制，等待重试 (${i + 1}/${MAX_RETRIES})...`);
        await sleep(...RETRY_DELAY);
        continue;
      }
      throw new Error(`HTTP ${resp.status}`);
    }
  }

  // ===== 开始爬取 =====
  console.log('🚀 开始爬取评论...');
  let currentToken = INIT_TOKEN;
  const allComments = [];
  let cursor = '', page = 0, totalSub = 0, incompleteSub = 0;

  while (true) {
    page++;
    if (page > 1) await sleep(...REQUEST_DELAY);

    const path = `/api/sns/web/v2/comment/page?note_id=${NOTE_ID}&cursor=${cursor}&top_comment_id=&image_formats=jpg,webp,avif&xsec_token=${encodeURIComponent(currentToken)}`;
    let data;
    try { data = await apiGet(path); } catch(e) { console.log(`❌ 主评论第${page}页异常: ${e.message}`); break; }
    if (data.code !== 0) { console.log(`❌ 主评论第${page}页: code=${data.code} ${data.msg}`); break; }

    if (data.data.xsec_token) currentToken = data.data.xsec_token;
    const comments = data.data.comments || [];
    console.log(`📄 主评论第${page}页: ${comments.length}条 (已发${requestCount}次请求)`);

    for (const comment of comments) {
      if (comment.sub_comment_has_more) {
        let subCursor = comment.sub_comment_cursor || '', subPage = 0;
        const existingIds = new Set((comment.sub_comments || []).map(s => s.id));

        while (true) {
          subPage++;
          await sleep(...REQUEST_DELAY);
          const subPath = `/api/sns/web/v2/comment/sub/page?note_id=${NOTE_ID}&root_comment_id=${comment.id}&num=10&cursor=${subCursor}&image_formats=jpg,webp,avif&top_comment_id=&xsec_token=${encodeURIComponent(currentToken)}`;
          try {
            const subData = await apiGet(subPath);
            if (subData.code !== 0) { console.log(`  ⚠️ 子评论失败: ${subData.msg}`); incompleteSub++; break; }
            const subs = subData.data.comments || [];
            for (const s of subs) { if (!existingIds.has(s.id)) { (comment.sub_comments = comment.sub_comments || []).push(s); existingIds.add(s.id); } }
            console.log(`  💬 子评论(${comment.id.slice(-6)})第${subPage}页: +${subs.length}, 累计${comment.sub_comments?.length || 0}`);
            if (!subData.data.has_more) break;
            subCursor = subData.data.cursor || '';
            if (!subCursor) break;
            if (subData.data.xsec_token) currentToken = subData.data.xsec_token;
          } catch(e) { console.log(`  ❌ 子评论异常: ${e.message}`); incompleteSub++; break; }
        }
        comment.sub_comment_has_more = false;
      }
      totalSub += (comment.sub_comments || []).length;
      allComments.push(comment);
    }

    // 每页更新结果到全局
    window._crawlResult = {
      note_id: NOTE_ID,
      total_comments: allComments.length,
      total_sub_comments: totalSub,
      incomplete_sub_comments: incompleteSub,
      comments: allComments
    };

    if (!data.data.has_more) { console.log('✅ 所有主评论已获取完毕'); break; }
    cursor = data.data.cursor || '';
    if (!cursor) { console.log('⚠️ cursor 为空'); break; }
  }

  console.log(`\n${'='.repeat(50)}`);
  console.log(`✅ 爬取完成!`);
  console.log(`主评论: ${allComments.length} 条`);
  console.log(`子评论: ${totalSub} 条`);
  console.log(`总请求: ${requestCount} 次`);
  if (incompleteSub > 0) console.log(`⚠️ 不完整: ${incompleteSub} 条`);
  console.log(`结果保存在 window._crawlResult`);
  console.log(`执行 copy(JSON.stringify(window._crawlResult)) 复制到剪贴板`);
  console.log(`${'='.repeat(50)}`);
})();
