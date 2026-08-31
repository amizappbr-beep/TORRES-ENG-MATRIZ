// Meta Pixel (browser). Ativa somente quando REACT_APP_META_PIXEL_ID existir.
const PIXEL_ID = process.env.REACT_APP_META_PIXEL_ID;

export function initMetaPixel() {
  if (!PIXEL_ID || typeof window === "undefined" || window.fbq) return;
  !(function (f, b, e, v, n, t, s) {
    if (f.fbq) return;
    n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n;
    n.loaded = true;
    n.version = "2.0";
    n.queue = [];
    t = b.createElement(e);
    t.async = true;
    t.src = v;
    s = b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t, s);
  })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
  window.fbq("init", PIXEL_ID);
  window.fbq("track", "PageView");
}

export function metaTrack(event, params = {}) {
  if (typeof window !== "undefined" && window.fbq && PIXEL_ID) {
    window.fbq("track", event, params);
  }
}

// Mapeia os eventos internos do funil para eventos padrão do Meta Pixel.
const MAP = {
  quiz_started: ["ViewContent", { content_name: "Quiz Feirão", content_category: "quiz" }],
  quiz_completed: ["ViewContent", { content_name: "Quiz concluído", content_category: "quiz" }],
  lead_created: ["Lead", {}],
  event_signup: ["Schedule", {}],
  appointment_created: ["Schedule", {}],
  whatsapp_clicked: ["Contact", { contact_method: "whatsapp" }],
};

export function metaFromFunnel(eventName, extra = {}) {
  const m = MAP[eventName];
  if (!m) return; // page_view já é disparado pelo init
  metaTrack(m[0], { ...m[1], ...extra });
}
