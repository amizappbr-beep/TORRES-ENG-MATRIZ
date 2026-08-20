import axios from "axios";

const RAW = process.env.REACT_APP_BACKEND_URL || "";
const BASE = RAW.replace(/\/$/, "");

export const api = axios.create({ baseURL: `${BASE}/api` });

// ---- Session id (persistent per browser) ----
export function getSessionId() {
  let sid = localStorage.getItem("feirao_sid");
  if (!sid) {
    sid =
      "s_" +
      Date.now().toString(36) +
      Math.random().toString(36).slice(2, 8);
    localStorage.setItem("feirao_sid", sid);
  }
  return sid;
}

// ---- UTM capture (persist first-touch) ----
export function captureUTM() {
  const params = new URLSearchParams(window.location.search);
  const keys = ["source", "medium", "campaign", "term", "content"];
  const utm = {};
  let found = false;
  keys.forEach((k) => {
    const v = params.get(`utm_${k}`) || params.get(k);
    if (v) {
      utm[k] = v;
      found = true;
    }
  });
  const origem = params.get("origem");
  if (origem) utm.origem = origem;
  if (found || origem) {
    localStorage.setItem("feirao_utm", JSON.stringify(utm));
  }
  return getUTM();
}

export function getUTM() {
  try {
    return JSON.parse(localStorage.getItem("feirao_utm") || "{}");
  } catch (_) {
    return {};
  }
}

// ---- Analytics event ----
export async function track(event, extra = {}) {
  try {
    const utm = getUTM();
    await api.post("/feirao/events", {
      event,
      session_id: getSessionId(),
      utm,
      origem: utm.origem || null,
      ...extra,
    });
  } catch (_) {
    /* analytics must never break UX */
  }
}

export async function fetchConfig() {
  const { data } = await api.get("/feirao/config");
  return data;
}
