webpackJsonp([4], {
    15: function (e, t, n) {
        "use strict";
        (function (e) {
            function o(e) {
                return e && e.__esModule ? e : {default: e}
            }

            function c(t) {
                return new u.default(function (o, c) {
                    console.log("init weixin"), e.get("http://wechat-sport-dbg.huangloong.com/api", function (e) {
                        d = e, p = Date.now() / 1e3 | 0;
                        var o = "jsapi_ticket=" + d + "&noncestr=" + f + "&timestamp=" + p + "&url=http://wechat-sport-dbg.huangloong.com/" + t,
                            c = n(38);
                        g = c(o), s.default.config({
                            debug: !1,
                            beta: !0,
                            appId: l,
                            timestamp: p,
                            nonceStr: f,
                            signature: g,
                            jsApiList: ["uploadImage", "openWXDeviceLib", "closeWXDeviceLib", "getWXDeviceInfos", "startScanWXDevice", "stopScanWXDevice", "connectWXDevice", "disconnectWXDevice", "onReceiveDataFromWXDevice", "onScanWXDeviceResult", "onWXDeviceStateChange", "getWXDeviceTicket", "onWXDeviceBluetoothStateChange", "sendDataToWXDevice"]
                        })
                    }), s.default.ready(function () {
                        return o()
                    }), s.default.error(function (e) {
                        return c(e)
                    })
                })
            }

            function a() {
                return u.default.resolve()
            }

            Object.defineProperty(t, "__esModule", {value: !0}), t.wx = void 0;
            var i = n(22), u = o(i);
            t.initWeixinJssdk = c, t.debugWeixinMock = a;
            var r = n(39), s = o(r);
            t.wx = s.default;
            var l = "wxe4f18fc7330cbf75", d = "", f = "Wm3WZYTPz0wzccnW", g = "", p = ""
        }).call(t, n(40))
    }, 161: function (e, t, n) {
        "use strict";
        n(83);
        var o = n(2), c = n(7), a = function (e) {
            return e && e.__esModule ? e : {default: e}
        }(c);
        (0, o.addEntry)(function () {
            (0, a.default)("#o2_loading").remove(), (0, a.default)("#o2_main").removeClass("hide")
        }), (0, o.start)()
    }, 2: function (e, t, n) {
        "use strict";

        function o(e) {
            return e && e.__esModule ? e : {default: e}
        }

        function c() {
            (0, u.debugWeixinMock)().then(function () {
                console.log("ES6 const test: " + p), console.log("ES7 exp operator test: " + Math.pow(p, 2)), console.log("ES6 array API test: " + (0, i.default)("foo")), console.log("ES6 template test: " + p), console.log("wx jssdk ready")
            }).then(function () {
                return v(f)
            }).catch(function (e) {
                console.log(e), v(g)
            })
        }

        var a = n(21), i = o(a), u = n(15), r = n(36), s = o(r), l = n(37), d = o(l), f = [], g = [], p = 3.1415926,
            v = (0, s.default)(function (e) {
                e.map(function (e) {
                    console.debug("issue callback " + e), e(), console.debug("callback returned")
                })
            }), W = (0, s.default)(function (e, t) {
                e.push(t)
            }), b = W(f), m = W(g), D = new d.default({resources: [], concurrency: 4, perMinTime: 1e3});
        D.addProgressListener(function (e, t) {
            console.log("loaded", e, t, e / t)
        }), D.addCompletionListener(function () {
            c()
        });
        var h = function () {
            return D.start()
        };
        e.exports = {start: h, addEntry: b, addFallback: m}
    }, 83: function (e, t) {
    }
}, [161]);