// ==UserScript==
// @name         小红书认证参数调试器 v2
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  调试小红书X-s-common等认证参数的生成（请求前拦截）
// @author       你
// @match        https://www.xiaohongshu.com/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    console.log('🔍 小红书认证参数调试器 v2 已启动');

    // 1. 拦截 XMLHttpRequest - 在请求发送前拦截
    const originalXHROpen = XMLHttpRequest.prototype.open;
    const originalXHRSend = XMLHttpRequest.prototype.send;
    const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

    XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
        this._url = url;
        this._method = method;
        this._requestHeaders = {};
        return originalXHROpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        this._requestHeaders = this._requestHeaders || {};
        this._requestHeaders[header.toLowerCase()] = value;
        
        // 监控关键认证参数
        if (header.toLowerCase() === 'x-s-common') {
            console.log('🔥 [XMLHttpRequest] 设置X-s-common:', value);
            console.log('📍 [XMLHttpRequest] 调用栈:', new Error().stack);
            console.log('🌐 [XMLHttpRequest] 请求URL:', this._url);
            console.log('📋 [XMLHttpRequest] 当前所有头部:', this._requestHeaders);
            debugger; // 在这里触发断点
        }
        
        if (header.toLowerCase() === 'x-s') {
            console.log('📝 [XMLHttpRequest] 设置X-s:', value);
        }
        
        if (header.toLowerCase() === 'x-t') {
            console.log('⏰ [XMLHttpRequest] 设置X-t:', value);
        }
        
        return originalSetRequestHeader.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(data) {
        const xhr = this;
        
        // 在发送前检查是否是子评论API
        if (xhr._url && xhr._url.includes('/api/sns/web/v2/comment/sub/page')) {
            console.log('🎯 [XMLHttpRequest] 即将发送子评论API请求:');
            console.log('URL:', xhr._url);
            console.log('Method:', xhr._method);
            console.log('Request Headers:', xhr._requestHeaders);
            console.log('Request Data:', data);
            
            // 检查是否有X-s-common
            const xSCommon = xhr._requestHeaders['x-s-common'];
            if (xSCommon) {
                console.log('✅ [XMLHttpRequest] 请求包含X-s-common:', xSCommon);
            } else {
                console.log('❌ [XMLHttpRequest] 请求缺少X-s-common');
            }
            
            // 在发送前触发断点，这样可以看到完整的请求状态
            debugger;
        }
        
        // 拦截响应
        const originalOnReadyStateChange = xhr.onreadystatechange;
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                // 检查是否是子评论API
                if (xhr._url && xhr._url.includes('/api/sns/web/v2/comment/sub/page')) {
                    console.log('📡 [XMLHttpRequest] 收到子评论API响应:');
                    console.log('Response Status:', xhr.status);
                    console.log('Response Headers:', xhr.getAllResponseHeaders());
                    
                    if (xhr.status === 200) {
                        console.log('✅ [XMLHttpRequest] 请求成功');
                        try {
                            const response = JSON.parse(xhr.responseText);
                            console.log('Response Data:', response);
                        } catch (e) {
                            console.log('Response Text:', xhr.responseText);
                        }
                    } else {
                        console.log('❌ [XMLHttpRequest] 请求失败:', xhr.status);
                    }
                }
            }
            
            if (originalOnReadyStateChange) {
                originalOnReadyStateChange.apply(this, arguments);
            }
        };

        return originalXHRSend.apply(this, arguments);
    };

    // 2. 拦截 fetch API - 在请求前拦截
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        // 检查是否是子评论API
        if (typeof url === 'string' && url.includes('/api/sns/web/v2/comment/sub/page')) {
            console.log('🎯 [Fetch] 检测到子评论API请求:');
            console.log('URL:', url);
            console.log('Options:', options);
            
            if (options && options.headers) {
                const headers = typeof options.headers === 'object' ? options.headers : {};
                
                // 检查X-s-common
                const xSCommon = headers['X-s-common'] || headers['x-s-common'];
                if (xSCommon) {
                    console.log('🔥 [Fetch] 发现X-s-common:', xSCommon);
                    console.log('📍 [Fetch] 调用栈:', new Error().stack);
                    console.log('📋 [Fetch] 完整头部:', headers);
                    debugger; // 在这里触发断点
                } else {
                    console.log('❌ [Fetch] 未发现X-s-common');
                }
                
                // 显示所有头部
                console.log('📋 [Fetch] 所有请求头:');
                Object.keys(headers).forEach(key => {
                    console.log(`   ${key}: ${headers[key]}`);
                });
            }
            
            // 在发送前触发断点
            debugger;
        }

        return originalFetch.apply(this, arguments).then(response => {
            // 检查响应头
            if (typeof url === 'string' && url.includes('/api/sns/web/v2/comment/sub/page')) {
                console.log('📡 [Fetch] 收到响应:');
                console.log('Response Status:', response.status);
                console.log('Response Headers:', response.headers);
                
                if (response.status === 200) {
                    console.log('✅ [Fetch] 请求成功');
                    // 克隆响应以便读取body
                    const clonedResponse = response.clone();
                    clonedResponse.json().then(data => {
                        console.log('Response Data:', data);
                    }).catch(e => {
                        console.log('无法解析响应JSON:', e);
                    });
                } else {
                    console.log('❌ [Fetch] 请求失败:', response.status);
                }
            }
            
            return response;
        }).catch(error => {
            console.log('🚫 [Fetch] 请求异常:', error);
            throw error;
        });
    };

    // 3. 监控Headers对象的操作
    const originalHeadersSet = Headers.prototype.set;
    Headers.prototype.set = function(name, value) {
        if (name.toLowerCase() === 'x-s-common') {
            console.log('🔥 [Headers] 设置X-s-common:', value);
            console.log('📍 [Headers] 调用栈:', new Error().stack);
            debugger;
        }
        return originalHeadersSet.apply(this, arguments);
    };

    // 4. 监控Request对象
    const originalRequest = Request;
    window.Request = function(input, init) {
        if (typeof input === 'string' && input.includes('/api/sns/web/v2/comment/sub/page')) {
            console.log('🎯 [Request] 创建子评论API请求:');
            console.log('Input:', input);
            console.log('Init:', init);
            
            if (init && init.headers) {
                const xSCommon = init.headers['X-s-common'] || init.headers['x-s-common'];
                if (xSCommon) {
                    console.log('🔥 [Request] 发现X-s-common:', xSCommon);
                    debugger;
                }
            }
        }
        return new originalRequest(input, init);
    };

    // 5. 监控关键函数调用
    const originalFunction = Function.prototype.constructor;
    Function.prototype.constructor = function(...args) {
        const func = originalFunction.apply(this, args);
        
        // 检查函数体是否包含关键词
        const funcStr = args[0] || '';
        if (funcStr.includes('x-s-common') || funcStr.includes('seccore_signv2')) {
            console.log('🔍 发现可疑函数定义:', funcStr.substring(0, 200));
            debugger;
        }
        
        return func;
    };

    // 6. 监控页面加载完成后的API调用
    window.addEventListener('load', function() {
        console.log('📄 页面加载完成，开始监控子评论展开操作');
        
        // 监听所有点击事件
        document.addEventListener('click', function(e) {
            // 检查是否点击了展开子评论的按钮
            const target = e.target;
            if (target && (
                target.textContent.includes('展开') ||
                target.textContent.includes('回复') ||
                target.closest('.comment-item') ||
                target.closest('[data-testid*="comment"]') ||
                target.closest('[class*="comment"]')
            )) {
                console.log('🖱️ 检测到可能的评论相关点击:', target.textContent);
                // 延迟一点，等待API调用
                setTimeout(() => {
                    console.log('⏰ 等待API调用...');
                }, 100);
            }
        }, true);
    });

    console.log('✅ 调试器 v2 初始化完成');
    console.log('💡 请展开子评论，脚本会在设置X-s-common时触发断点');
    console.log('🔥 断点现在会在请求发送前触发，可以看到完整的认证参数');

})();