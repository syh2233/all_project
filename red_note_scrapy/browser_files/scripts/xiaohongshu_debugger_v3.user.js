// ==UserScript==
// @name         小红书X-s-common完整调试器
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  完整调试小红书X-s-common参数生成
// @author       你
// @match        https://www.xiaohongshu.com/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    console.log('🔍 小红书X-s-common完整调试器 v3 已启动');

    // 存储捕获的X-s-common值
    let capturedXSCommon = null;

    // 拦截 XMLHttpRequest
    const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        
        // 当设置X-s-common时触发断点
        if (header.toLowerCase() === 'x-s-common') {
            capturedXSCommon = value;
            
            console.log('🎯🎯🎯 发现X-s-common! 🎯🎯🎯');
            console.log('X-s-common值:', value);
            console.log('完整调用栈:');
            console.log(new Error().stack);
            
            // 获取请求信息
            if (this._url) {
                console.log('请求URL:', this._url);
                console.log('请求方法:', this._method || 'GET');
            }
            
            // 显示更多调试信息
            console.log('📋 X-s-common分析:');
            console.log('- 长度:', value.length);
            console.log('- 前20字符:', value.substring(0, 20));
            console.log('- 后20字符:', value.substring(value.length - 20));
            console.log('- 是否包含XYS_:', value.startsWith('XYS_'));
            console.log('- 包含重复模式:', /(.)\1{3,}/.test(value));
            
            // 尝试Base64解码
            try {
                const decoded = atob(value);
                console.log('Base64解码结果:', decoded);
            } catch (e) {
                console.log('不是标准Base64:', e.message);
                
                // 尝试去除可能的填充
                try {
                    const cleaned = value.replace(/=+$/, '');
                    const decoded2 = atob(cleaned);
                    console.log('清理后Base64解码:', decoded2);
                } catch (e2) {
                    console.log('清理后仍然不是Base64:', e2.message);
                }
            }
            
            // 分析字符串特征
            console.log('🔍 字符串特征分析:');
            const charCount = {};
            for (let char of value) {
                charCount[char] = (charCount[char] || 0) + 1;
            }
            const sortedChars = Object.entries(charCount)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            console.log('出现频率最高的字符:', sortedChars);
            
            // 查看时间戳相关信息
            console.log('⏰ 时间戳分析:');
            console.log('- 当前时间戳:', Date.now());
            console.log('- 当前时间:', new Date().toISOString());
            console.log('- 时间戳长度:', Date.now().toString().length);
            
            // 🔥 在这里触发断点
            debugger;
        }
        
        return originalSetRequestHeader.apply(this, arguments);
    };

    // 在全局作用域暴露调试函数
    window.debugXSCommon = function() {
        if (capturedXSCommon) {
            console.log('上次捕获的X-s-common:', capturedXSCommon);
            
            // 尝试各种解码方式
            console.log('🔍 尝试各种解码方式:');
            
            // 1. 标准Base64
            try {
                console.log('1. 标准Base64:', atob(capturedXSCommon));
            } catch (e) {
                console.log('1. 标准Base64失败:', e.message);
            }
            
            // 2. URL Safe Base64
            try {
                const urlSafe = capturedXSCommon.replace(/-/g, '+').replace(/_/g, '/');
                console.log('2. URL Safe Base64:', atob(urlSafe));
            } catch (e) {
                console.log('2. URL Safe Base64失败:', e.message);
            }
            
            // 3. 去除XYS_前缀
            if (capturedXSCommon.startsWith('XYS_')) {
                try {
                    const withoutPrefix = capturedXSCommon.substring(4);
                    console.log('3. 去除XYS_前缀:', atob(withoutPrefix));
                } catch (e) {
                    console.log('3. 去除XYS_前缀失败:', e.message);
                }
            }
            
            // 4. 分析可能的结构
            console.log('4. 可能的结构分析:');
            const segments = capturedXSCommon.match(/.{1,50}/g);
            console.log('分段显示:', segments);
            
            // 5. 查找可能的模式
            console.log('5. 模式分析:');
            const patterns = [
                /\d{13}/, // 时间戳
                /[a-f0-9]{32}/i, // MD5
                /[a-f0-9]{40}/i, // SHA1
                /[a-f0-9]{64}/i, // SHA256
                /[A-Za-z0-9+/]{20}={0,2}/ // Base64片段
            ];
            
            patterns.forEach((pattern, index) => {
                const matches = capturedXSCommon.match(pattern);
                if (matches) {
                    console.log(`   模式${index + 1} (${pattern}):`, matches);
                }
            });
            
        } else {
            console.log('还没有捕获到X-s-common，请先展开子评论');
        }
    };

    console.log('✅ 调试器 v3 初始化完成');
    console.log('💡 使用方法:');
    console.log('   1. 展开子评论触发自动断点');
    console.log('   2. 手动调用 debugXSCommon() 分析上次捕获的值');

})();