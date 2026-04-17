!function() {
    "use strict";
    var t, n, o, a, i, c, u, l, s = {}, d = {};
    function __webpack_require__(t) {
        var n = d[t];
        if (void 0 !== n)
            return n.exports;
        var o = d[t] = {
            id: t,
            loaded: !1,
            exports: {}
        };
        return s[t].call(o.exports, o, o.exports, __webpack_require__),
        o.loaded = !0,
        o.exports
    }
    __webpack_require__.m = s,
    __webpack_require__.n = function(t) {
        var n = t && t.__esModule ? function() {
            return t.default
        }
        : function() {
            return t
        }
        ;
        return __webpack_require__.d(n, {
            a: n
        }),
        n
    }
    ,
    n = Object.getPrototypeOf ? function(t) {
        return Object.getPrototypeOf(t)
    }
    : function(t) {
        return t.__proto__
    }
    ,
    __webpack_require__.t = function(o, a) {
        if (1 & a && (o = this(o)),
        8 & a || "object" == typeof o && o && (4 & a && o.__esModule || 16 & a && "function" == typeof o.then))
            return o;
        var i = Object.create(null);
        __webpack_require__.r(i);
        var c = {};
        t = t || [null, n({}), n([]), n(n)];
        for (var u = 2 & a && o; "object" == typeof u && !~t.indexOf(u); u = n(u))
            Object.getOwnPropertyNames(u).forEach(function(t) {
                c[t] = function() {
                    return o[t]
                }
            });
        return c.default = function() {
            return o
        }
        ,
        __webpack_require__.d(i, c),
        i
    }
    ,
    __webpack_require__.d = function(t, n) {
        for (var o in n)
            __webpack_require__.o(n, o) && !__webpack_require__.o(t, o) && Object.defineProperty(t, o, {
                enumerable: !0,
                get: n[o]
            })
    }
    ,
    __webpack_require__.f = {},
    __webpack_require__.e = function(t) {
        return Promise.all(Object.keys(__webpack_require__.f).reduce(function(n, o) {
            return __webpack_require__.f[o](t, n),
            n
        }, []))
    }
    ,
    __webpack_require__.u = function(t) {
        return "resource/js/async/" + (({
            182: "xhs-web-player",
            37: "library-launcher",
            437: "minor",
            44: "Note",
            447: "Track",
            574: "Explore",
            602: "Search",
            641: "Notification",
            656: "FeedToNote",
            775: "User",
            820: "NPS",
            831: "Board",
            906: "Login"
        })[t] || t) + "." + ({
            106: "6772ccf0",
            147: "2e7eaaa2",
            182: "bae3e2fc",
            19: "ddff14d1",
            218: "408fde30",
            264: "abb818b7",
            291: "7fdd45f5",
            294: "94bd8aa6",
            355: "e0e14cee",
            366: "0dee4632",
            37: "a774e33d",
            399: "71b017df",
            42: "15ce8770",
            436: "7bddfb45",
            437: "205642a6",
            44: "457d2fea",
            447: "9eb5ab04",
            574: "7f88a48b",
            594: "5a05027b",
            602: "743e0aac",
            641: "d2b60711",
            656: "011e1083",
            688: "bb985b64",
            75: "f80b305c",
            772: "7451eea2",
            775: "8b0c710b",
            820: "0f3b7535",
            831: "183c3e22",
            901: "4a92d0d6",
            906: "0e4a2e7b",
            919: "16ac3b2d",
            937: "d84b6fcb",
            953: "c4304ecb"
        })[t] + ".js"
    }
    ,
    __webpack_require__.miniCssF = function(t) {
        return "resource/css/async/" + (({
            437: "minor",
            44: "Note",
            574: "Explore",
            602: "Search",
            641: "Notification",
            656: "FeedToNote",
            775: "User",
            820: "NPS",
            831: "Board",
            906: "Login"
        })[t] || t) + "." + ({
            355: "1a9a769f",
            42: "1b2bf9e1",
            437: "a7f732ec",
            44: "12c00534",
            574: "30c1e8ce",
            602: "84e03d37",
            641: "aa311d0c",
            656: "a47e232f",
            75: "693a9a9c",
            772: "db47c221",
            775: "3830129f",
            820: "0fee7ba1",
            831: "c56ea05c",
            906: "c2772494",
            937: "de1aa713",
            953: "272459c1"
        })[t] + ".css"
    }
    ,
    __webpack_require__.h = function() {
        return "0bc06c503cbbe056"
    }
    ,
    __webpack_require__.g = function() {
        if ("object" == typeof globalThis)
            return globalThis;
        try {
            return this || Function("return this")()
        } catch (t) {
            if ("object" == typeof window)
                return window
        }
    }(),
    __webpack_require__.o = function(t, n) {
        return Object.prototype.hasOwnProperty.call(t, n)
    }
    ,
    o = {},
    a = "xhs-pc-web:",
    __webpack_require__.l = function(t, n, i, c) {
        if (o[t]) {
            o[t].push(n);
            return
        }
        if (void 0 !== i) {
            for (var u, l, s = document.getElementsByTagName("script"), d = 0; d < s.length; d++) {
                var b = s[d];
                if (b.getAttribute("src") == t || b.getAttribute("data-webpack") == a + i) {
                    u = b;
                    break
                }
            }
        }
        !u && (l = !0,
        (u = document.createElement("script")).charset = "utf-8",
        u.timeout = 120,
        __webpack_require__.nc && u.setAttribute("nonce", __webpack_require__.nc),
        u.setAttribute("data-webpack", a + i),
        u.src = t),
        o[t] = [n];
        var onScriptComplete = function(n, a) {
            u.onerror = u.onload = null,
            clearTimeout(w);
            var i = o[t];
            if (delete o[t],
            u.parentNode && u.parentNode.removeChild(u),
            i && i.forEach(function(t) {
                return t(a)
            }),
            n)
                return n(a)
        }
          , w = setTimeout(onScriptComplete.bind(null, void 0, {
            type: "timeout",
            target: u
        }), 12e4);
        u.onerror = onScriptComplete.bind(null, u.onerror),
        u.onload = onScriptComplete.bind(null, u.onload),
        l && document.head.appendChild(u)
    }
    ,
    __webpack_require__.r = function(t) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
            value: "Module"
        }),
        Object.defineProperty(t, "__esModule", {
            value: !0
        })
    }
    ,
    __webpack_require__.nmd = function(t) {
        return t.paths = [],
        !t.children && (t.children = []),
        t
    }
    ,
    i = [],
    __webpack_require__.O = function(t, n, o, a) {
        if (n) {
            a = a || 0;
            for (var c = i.length; c > 0 && i[c - 1][2] > a; c--)
                i[c] = i[c - 1];
            i[c] = [n, o, a];
            return
        }
        for (var u = 1 / 0, c = 0; c < i.length; c++) {
            for (var n = i[c][0], o = i[c][1], a = i[c][2], l = !0, s = 0; s < n.length; s++)
                (!1 & a || u >= a) && Object.keys(__webpack_require__.O).every(function(t) {
                    return __webpack_require__.O[t](n[s])
                }) ? n.splice(s--, 1) : (l = !1,
                a < u && (u = a));
            if (l) {
                i.splice(c--, 1);
                var d = o();
                void 0 !== d && (t = d)
            }
        }
        return t
    }
    ,
    !function() {
        function r(t) {
            for (var n = 1; n < arguments.length; n++) {
                var o = null != arguments[n] ? arguments[n] : {}
                  , a = Object.keys(o);
                "function" == typeof Object.getOwnPropertySymbols && (a = a.concat(Object.getOwnPropertySymbols(o).filter(function(t) {
                    return Object.getOwnPropertyDescriptor(o, t).enumerable
                }))),
                a.forEach(function(n) {
                    var a;
                    a = o[n],
                    n in t ? Object.defineProperty(t, n, {
                        value: a,
                        enumerable: !0,
                        configurable: !0,
                        writable: !0
                    }) : t[n] = a
                })
            }
            return t
        }
        function e(t, n) {
            return n = null != n ? n : {},
            Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : (function(t, n) {
                var o = Object.keys(t);
                if (Object.getOwnPropertySymbols) {
                    var a = Object.getOwnPropertySymbols(t);
                    o.push.apply(o, a)
                }
                return o
            }
            )(Object(n)).forEach(function(o) {
                Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o))
            }),
            t
        }
        __webpack_require__.p = "https://fe-static.xhscdn.com/formula-static/xhs-pc-web/public/";
        var t, n, o, a, i, c, u, l, f = function() {
            if ("undefined" != typeof window) {
                var t, n, o = null === (t = window.eaglet) || void 0 === t ? void 0 : t.push;
                return o || (o = null === (n = window.insight) || void 0 === n ? void 0 : n.push),
                o ? function(t) {
                    var n;
                    return o(e(r({}, n = t), {
                        context_artifactName: "formula",
                        context_artifactVersion: "4.0.16",
                        measurement_data: e(r({}, n.measurement_data), {
                            packageName: "xhs-pc-web",
                            packageVersion: "4.79.0"
                        })
                    }), "ApmXrayTracker")
                }
                : void 0
            }
        }, s = "FORMULA_ASSETS_LOAD_ERROR", m = function() {
            var t = localStorage.getItem(s);
            return t ? JSON.parse(t) : []
        };
        function p(t) {
            try {
                var n = f();
                if (n)
                    n(t);
                else {
                    var o = m();
                    if (o.length >= 1e3)
                        return;
                    o.push(t),
                    localStorage.setItem(s, JSON.stringify(o))
                }
            } catch (n) {
                console.error({
                    error: n,
                    errorData: t
                })
            }
        }
        function y(t, n) {
            (null == n || n > t.length) && (n = t.length);
            for (var o = 0, a = Array(n); o < n; o++)
                a[o] = t[o];
            return a
        }
        t = function(t) {
            if (l.push(t),
            !u) {
                var n = __webpack_require__.f.miniCss;
                __webpack_require__.f.miniCss = function(t) {
                    for (var o = arguments.length, a = Array(o > 1 ? o - 1 : 0), i = 1; i < o; i++)
                        a[i - 1] = arguments[i];
                    l.includes(t) || n.apply(void 0, [t].concat(function(t) {
                        if (Array.isArray(t))
                            return y(t)
                    }(a) || function(t) {
                        if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"])
                            return Array.from(t)
                    }(a) || function(t, n) {
                        if (t) {
                            if ("string" == typeof t)
                                return y(t, void 0);
                            var o = Object.prototype.toString.call(t).slice(8, -1);
                            if ("Object" === o && t.constructor && (o = t.constructor.name),
                            "Map" === o || "Set" === o)
                                return Array.from(o);
                            if ("Arguments" === o || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(o))
                                return y(t, void 0)
                        }
                    }(a) || function() {
                        throw TypeError("Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
                    }()))
                }
                ,
                u = !0
            }
        }
        ,
        n = {},
        o = {
            path: "undefined" == typeof window ? "" : window.location.href,
            resourceType: "js"
        },
        a = Object.assign,
        i = __webpack_require__.l,
        c = __webpack_require__.e,
        __webpack_require__.l = function(t, c, u, l) {
            var _ = function(o) {
                if (o && n[t]) {
                    var i = n[t].newUrl
                      , u = Date.now() - n[t].startTime;
                    "error" === o.type ? p({
                        measurement_name: "reload_resource_error",
                        measurement_data: a(s, {
                            timestamp: String(Date.now()),
                            retryErrorType: "retryOnloadError",
                            retryResourceUrl: i
                        })
                    }) : (p({
                        measurement_name: "reload_resource_duration",
                        measurement_data: a(s, {
                            duration: u,
                            timestamp: String(Date.now()),
                            retryResourceUrl: i
                        })
                    }),
                    c(o))
                }
            };
            i(t, function(o) {
                if (o && !n[t]) {
                    if ("error" !== o.type)
                        return c(o);
                    var d = Date.now();
                    p({
                        measurement_name: "biz_load_error_count",
                        measurement_data: a(s, {
                            timestamp: String(d)
                        })
                    });
                    var b = function(t) {
                        if (t) {
                            var n = "//fe-static.xhscdn.com";
                            return -1 !== t.indexOf(n) ? "".concat(t.replace(n, "//cdn.xiaohongshu.com"), "?business=fe&scene=feplatform") : void 0
                        }
                    }(t);
                    if (!b)
                        return p({
                            measurement_name: "reload_resource_error",
                            measurement_data: a(s, {
                                retryErrorType: "newUrlError",
                                timestamp: String(Date.now())
                            })
                        }),
                        c(o);
                    console.warn("Chunk load failed, retrying:", b),
                    n[t] = {
                        newUrl: b,
                        startTime: d
                    },
                    i(b, _, u, l)
                }
            }, u, l);
            var s = a(o, {
                resourceUrl: t
            })
        }
        ,
        __webpack_require__.e = function(n) {
            return c(n).catch(function(o) {
                return console.warn("Chunk loading failed, retrying for chunk:", n),
                console.warn(o),
                t(n),
                c(n)
            })
        }
        ,
        u = !1,
        l = []
    }(),
    __webpack_require__.rv = function() {
        return "1.2.5"
    }
    ,
    !function() {
        if ("undefined" != typeof document) {
            var createStylesheet = function(t, n, o, a, i) {
                var c = document.createElement("link");
                return c.rel = "stylesheet",
                c.type = "text/css",
                __webpack_require__.nc && (c.nonce = __webpack_require__.nc),
                c.onerror = c.onload = function(o) {
                    if (c.onerror = c.onload = null,
                    "load" === o.type)
                        a();
                    else {
                        var u = o && ("load" === o.type ? "missing" : o.type)
                          , l = o && o.target && o.target.href || n
                          , s = Error("Loading CSS chunk " + t + " failed.\\n(" + l + ")");
                        s.code = "CSS_CHUNK_LOAD_FAILED",
                        s.type = u,
                        s.request = l,
                        c.parentNode && c.parentNode.removeChild(c),
                        i(s)
                    }
                }
                ,
                c.href = n,
                o ? o.parentNode.insertBefore(c, o.nextSibling) : document.head.appendChild(c),
                c
            }
              , findStylesheet = function(t, n) {
                for (var o = document.getElementsByTagName("link"), a = 0; a < o.length; a++) {
                    var i = o[a]
                      , c = i.getAttribute("data-href") || i.getAttribute("href");
                    if ("stylesheet" === i.rel && (c === t || c === n))
                        return i
                }
                for (var u = document.getElementsByTagName("style"), a = 0; a < u.length; a++) {
                    var i = u[a]
                      , c = i.getAttribute("data-href");
                    if (c === t || c === n)
                        return i
                }
            }
              , t = {
                145: 0
            };
            __webpack_require__.f.miniCss = function(n, o) {
                if (t[n])
                    o.push(t[n]);
                else if (0 !== t[n] && ({
                    953: 1,
                    772: 1,
                    906: 1,
                    42: 1,
                    75: 1,
                    820: 1,
                    656: 1,
                    937: 1,
                    355: 1,
                    574: 1,
                    44: 1,
                    775: 1,
                    602: 1,
                    641: 1,
                    831: 1,
                    437: 1
                })[n]) {
                    var a;
                    o.push(t[n] = (a = n,
                    new Promise(function(t, n) {
                        var o = __webpack_require__.miniCssF(a)
                          , i = __webpack_require__.p + o;
                        if (findStylesheet(o, i))
                            return t();
                        createStylesheet(a, i, null, t, n)
                    }
                    )).then(function() {
                        t[n] = 0
                    }, function(o) {
                        throw delete t[n],
                        o
                    }))
                }
            }
        }
    }(),
    c = {
        145: 0
    },
    __webpack_require__.f.j = function(t, n) {
        var o = __webpack_require__.o(c, t) ? c[t] : void 0;
        if (0 !== o) {
            if (o)
                n.push(o[2]);
            else if (145 != t) {
                var a = new Promise(function(n, a) {
                    o = c[t] = [n, a]
                }
                );
                n.push(o[2] = a);
                var i = __webpack_require__.p + __webpack_require__.u(t)
                  , u = Error();
                __webpack_require__.l(i, function(n) {
                    if (__webpack_require__.o(c, t) && (0 !== (o = c[t]) && (c[t] = void 0),
                    o)) {
                        var a = n && ("load" === n.type ? "missing" : n.type)
                          , i = n && n.target && n.target.src;
                        u.message = "Loading chunk " + t + " failed.\n(" + a + ": " + i + ")",
                        u.name = "ChunkLoadError",
                        u.type = a,
                        u.request = i,
                        o[1](u)
                    }
                }, "chunk-" + t, t)
            } else
                c[t] = 0
        }
    }
    ,
    __webpack_require__.O.j = function(t) {
        return 0 === c[t]
    }
    ,
    u = function(t, n) {
        var o = n[0], a = n[1], i = n[2], u, l, s = 0;
        if (o.some(function(t) {
            return 0 !== c[t]
        })) {
            for (u in a)
                __webpack_require__.o(a, u) && (__webpack_require__.m[u] = a[u]);
            if (i)
                var d = i(__webpack_require__)
        }
        for (t && t(n); s < o.length; s++)
            l = o[s],
            __webpack_require__.o(c, l) && c[l] && c[l][0](),
            c[l] = 0;
        return __webpack_require__.O(d)
    }
    ,
    (l = self.webpackChunkxhs_pc_web = self.webpackChunkxhs_pc_web || []).forEach(u.bind(null, 0)),
    l.push = u.bind(null, l.push.bind(l)),
    __webpack_require__.ruid = "bundler=rspack@1.2.5"
}();

