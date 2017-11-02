webpackJsonp([1], {
    15: function (e, n, t) {
        "use strict";
        (function (e) {
            function o(e) {
                return e && e.__esModule ? e : {default: e}
            }

            function c(n) {
                return new u.default(function (o, c) {
                    console.log("init weixin"), e.get("http://wechat-sport-dbg.huangloong.com/api", function (e) {
                        d = e, g = Date.now() / 1e3 | 0;
                        var o = "jsapi_ticket=" + d + "&noncestr=" + f + "&timestamp=" + g + "&url=http://wechat-sport-dbg.huangloong.com/" + n,
                            c = t(38);
                        A = c(o), r.default.config({
                            debug: !1,
                            beta: !0,
                            appId: s,
                            timestamp: g,
                            nonceStr: f,
                            signature: A,
                            jsApiList: ["uploadImage", "openWXDeviceLib", "closeWXDeviceLib", "getWXDeviceInfos", "startScanWXDevice", "stopScanWXDevice", "connectWXDevice", "disconnectWXDevice", "onReceiveDataFromWXDevice", "onScanWXDeviceResult", "onWXDeviceStateChange", "getWXDeviceTicket", "onWXDeviceBluetoothStateChange", "sendDataToWXDevice"]
                        })
                    }), r.default.ready(function () {
                        return o()
                    }), r.default.error(function (e) {
                        return c(e)
                    })
                })
            }

            function a() {
                return u.default.resolve()
            }

            Object.defineProperty(n, "__esModule", {value: !0}), n.wx = void 0;
            var i = t(22), u = o(i);
            n.initWeixinJssdk = c, n.debugWeixinMock = a;
            var l = t(39), r = o(l);
            n.wx = r.default;
            var s = "wxe4f18fc7330cbf75", d = "", f = "Wm3WZYTPz0wzccnW", A = "", g = ""
        }).call(n, t(40))
    }, 159: function (e, n, t) {
        "use strict";
        t(81), t(16), t(84);
        var o = t(2), c = t(7), a = function (e) {
            return e && e.__esModule ? e : {default: e}
        }(c);
        (0, o.addEntry)(function () {
            (0, a.default)("#o2_loading").remove(), (0, a.default)("#o2_main").removeClass("hide")
        }), (0, o.start)()
    }, 16: function (e, n, t) {
        e.exports = t.p + "img/corgi-puppy-6.jpg?e93ff0"
    }, 2: function (e, n, t) {
        "use strict";

        function o(e) {
            return e && e.__esModule ? e : {default: e}
        }

        function c() {
            (0, u.debugWeixinMock)().then(function () {
                console.log("ES6 const test: " + g), console.log("ES7 exp operator test: " + Math.pow(g, 2)), console.log("ES6 array API test: " + (0, i.default)("foo")), console.log("ES6 template test: " + g), console.log("wx jssdk ready")
            }).then(function () {
                return p(f)
            }).catch(function (e) {
                console.log(e), p(A)
            })
        }

        var a = t(21), i = o(a), u = t(15), l = t(36), r = o(l), s = t(37), d = o(s), f = [], A = [], g = 3.1415926,
            p = (0, r.default)(function (e) {
                e.map(function (e) {
                    console.debug("issue callback " + e), e(), console.debug("callback returned")
                })
            }), v = (0, r.default)(function (e, n) {
                e.push(n)
            }), W = v(f), b = v(A), m = new d.default({resources: [], concurrency: 4, perMinTime: 1e3});
        m.addProgressListener(function (e, n) {
            console.log("loaded", e, n, e / n)
        }), m.addCompletionListener(function () {
            c()
        });
        var D = function () {
            return m.start()
        };
        e.exports = {start: D, addEntry: W, addFallback: b}
    }, 81: function (e, n) {
    }, 84: function (e, n) {
        e.exports = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADIAQMAAACXljzdAAAABlBMVEUAAAD///+l2Z/dAAABeklEQVRYR9XXvY1mIQxG4YMIbkgJlEJnA19nlEIJhDdAnA2Y/ZG2AcahnwjxypYBABdp8BVfKPJv3SlBtbkedUdn7vW07pYFpbmA8lmPo3haP0OStviS/TmyIdnDeibUe+RvQnpdQPH/7Fwnp3Z80yif9czcK//WnaKqG8j9C4B6WnfLItng0U7UAWGl22Xz+D3sdD2TYlhplHa1BJ2lwTOz7byK6KBeLTtqr0Aa5bOA0nac2Xa1hJOds8sXyY464GoBKG6eSdnxTYNKnFwuQe3s6MxuAKqLbLtANo9KfPnOtS04c+dq0TfZgk5KOzlxkXu9WnZ0UokvuRNVmzqKV0tYzyxtRx2lAVnD/eJ6JvXsl49vshNWul121M73DIE0AK4X1T8Xljr+TJeb5dTmmbnXRRrU71+4WYJq05fsRydUV7Jztyw41+HgC8j9vLBeIyfXruckJI2fIfEl96CO0lRtd8vvhKRB9U0Dwkr2erWcUv19I9YdvVx+AatrsheHQ+JsAAAAAElFTkSuQmCC"
    }
}, [159]);