import React, { useCallback, useEffect, useState } from "react";
import { useAdmin } from "./AdminContext";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { Loader2, RefreshCw, TrendingUp, DollarSign } from "lucide-react";

const EMP_LABELS = {
  viva: "Residencial Viva",
  alameda: "Alameda 500",
  life: "Life 740",
  aldeia: "Aldeia 350",
};
const CLASSE_COLORS = { A: "#059669", B: "#2563EB", C: "#D97706", D: "#94A3B8" };
const PERIODS = [
  { v: 7, l: "7 dias" },
  { v: 30, l: "30 dias" },
  { v: 90, l: "90 dias" },
];

function Kpi({ label, value, sub }) {
  return (
    <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-4 shadow-sm">
      <div className="text-xs font-semibold uppercase tracking-wide text-[color:var(--torres-muted)]">
        {label}
      </div>
      <div className="mt-1 text-2xl font-extrabold text-[color:var(--torres-ink)]">{value}</div>
      {sub && <div className="text-xs text-[color:var(--torres-muted)]">{sub}</div>}
    </div>
  );
}

function Bar({ label, value, max, color = "#0B2A4A" }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-[color:var(--torres-ink)]">{label}</span>
        <span className="font-bold tabular-nums text-[color:var(--torres-ink)]">{value}</span>
      </div>
      <div className="mt-1 h-2.5 w-full rounded-full bg-slate-100">
        <div className="h-full rounded-full" style={{ width: `${Math.max(pct, 2)}%`, background: color }} />
      </div>
    </div>
  );
}

export default function AnalyticsView() {
  const { axiosAdmin } = useAdmin();
  const [days, setDays] = useState(30);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [updatedAt, setUpdatedAt] = useState(null);

  const load = useCallback(
    async (silent = false) => {
      if (silent) setRefreshing(true);
      try {
        const r = await axiosAdmin.get(`/admin/feirao/analytics?days=${days}`);
        setData(r.data);
        setUpdatedAt(new Date());
      } catch (e) {
        if (e?.response?.status !== 401) console.error("Erro no analytics:", e);
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [axiosAdmin, days]
  );

  useEffect(() => {
    setLoading(true);
    load();
  }, [load]);

  // auto-refresh a cada 45s
  useEffect(() => {
    const id = setInterval(() => load(true), 45000);
    return () => clearInterval(id);
  }, [load]);

  if (loading) {
    return (
      <div className="flex min-h-[300px] items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-[#0B2A4A]" />
      </div>
    );
  }

  const kpis = data?.kpis || {};
  const funil = data?.funnel || {};
  const funnelMax = Math.max(1, ...Object.values(funil));
  const origem = data?.origem || [];
  const porEmp = data?.por_empreendimento || {};
  const classes = data?.classes || { A: 0, B: 0, C: 0, D: 0 };
  const series = data?.series || [];
  const convLead = funil.visitantes ? Math.round((kpis.leads_range / funil.visitantes) * 100) : 0;

  return (
    <div data-testid="admin-analytics-view" className="mx-auto max-w-[1600px] px-6 py-6 sm:px-10">
      {/* Header: período + refresh */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-[color:var(--torres-muted)]">
          <TrendingUp className="h-4 w-4" /> Analytics em tempo real
        </h2>
        <div className="flex items-center gap-2">
          <div className="flex rounded-full border border-[color:var(--torres-line)] bg-white p-0.5">
            {PERIODS.map((p) => (
              <button
                key={p.v}
                data-testid={`analytics-period-${p.v}`}
                onClick={() => setDays(p.v)}
                className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                  days === p.v ? "bg-[#0B2A4A] text-white" : "text-[color:var(--torres-muted)]"
                }`}
              >
                {p.l}
              </button>
            ))}
          </div>
          <button
            onClick={() => load(true)}
            className="flex items-center gap-1 rounded-full border border-[color:var(--torres-line)] bg-white px-3 py-1.5 text-xs font-semibold text-[color:var(--torres-ink)]"
            title="Atualizar agora"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} />
            {updatedAt ? updatedAt.toLocaleTimeString("pt-BR") : "Atualizar"}
          </button>
        </div>
      </div>

      {/* KPIs */}
      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        <Kpi label="Leads hoje" value={kpis.hoje ?? 0} />
        <Kpi label="Leads 7 dias" value={kpis.leads_7d ?? 0} />
        <Kpi label={`Leads ${days}d`} value={kpis.leads_range ?? 0} />
        <Kpi label="Total de leads" value={kpis.total ?? 0} />
        <Kpi label="Conversão" value={`${convLead}%`} sub="visitante → lead" />
        <Kpi label="Agendaram" value={kpis.agendaram ?? 0} />
      </div>

      {/* Série temporal */}
      <div className="mt-6 rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
        <h3 className="text-sm font-bold text-[color:var(--torres-ink)]">
          Leads e visitantes por dia
        </h3>
        <div className="mt-4 h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={series} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 11 }}
                tickFormatter={(d) => d.slice(5)}
                minTickGap={20}
              />
              <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
              <Tooltip />
              <Line type="monotone" dataKey="visitantes" stroke="#94A3B8" strokeWidth={2} dot={false} name="Visitantes" />
              <Line type="monotone" dataKey="leads" stroke="#0B2A4A" strokeWidth={2.5} dot={false} name="Leads" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        {/* Funil */}
        <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
          <h3 className="text-sm font-bold text-[color:var(--torres-ink)]">Funil de conversão</h3>
          <div className="mt-4 space-y-3">
            <Bar label="Visitantes" value={funil.visitantes || 0} max={funnelMax} />
            <Bar label="Iniciaram quiz" value={funil.iniciaram_quiz || 0} max={funnelMax} />
            <Bar label="Finalizaram quiz" value={funil.finalizaram_quiz || 0} max={funnelMax} />
            <Bar label="Cadastraram" value={funil.cadastraram || 0} max={funnelMax} />
            <Bar label="Agendaram" value={funil.agendaram || 0} max={funnelMax} />
            <Bar label="Clicaram no WhatsApp" value={funil.clicaram_whatsapp || 0} max={funnelMax} />
          </div>
        </div>

        {/* Origem + CPL */}
        <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
          <h3 className="text-sm font-bold text-[color:var(--torres-ink)]">Origem dos leads (UTM)</h3>
          <div className="mt-3 overflow-hidden rounded-xl border border-[color:var(--torres-line)]">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-left text-[11px] uppercase text-[color:var(--torres-muted)]">
                <tr>
                  <th className="px-3 py-2">Origem</th>
                  <th className="px-3 py-2">Campanha</th>
                  <th className="px-3 py-2 text-right">Leads</th>
                </tr>
              </thead>
              <tbody>
                {origem.length === 0 && (
                  <tr>
                    <td colSpan={3} className="px-3 py-4 text-center text-[color:var(--torres-muted)]">
                      Sem leads no período.
                    </td>
                  </tr>
                )}
                {origem.map((o, i) => (
                  <tr key={`${o.source}-${o.campaign}-${i}`} className="border-t border-[color:var(--torres-line)]">
                    <td className="px-3 py-2 font-medium text-[color:var(--torres-ink)]">{o.source}</td>
                    <td className="px-3 py-2 text-[color:var(--torres-muted)]">{o.campaign || "—"}</td>
                    <td className="px-3 py-2 text-right font-bold tabular-nums">{o.leads}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 flex items-start gap-2 rounded-xl bg-amber-50 p-3 text-xs text-amber-800">
            <DollarSign className="mt-0.5 h-4 w-4 flex-shrink-0" />
            <span>
              <b>Custo por Lead (CPL):</b> conecte a Meta Marketing API para puxar o
              investimento das campanhas e calcular o CPL automaticamente. (aguardando credenciais)
            </span>
          </div>
        </div>
      </div>

      {/* Distribuição */}
      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
          <h3 className="text-sm font-bold text-[color:var(--torres-ink)]">Por empreendimento</h3>
          <div className="mt-4 space-y-3">
            {Object.keys(EMP_LABELS).map((slug) => {
              const max = Math.max(1, ...Object.values(porEmp));
              return <Bar key={slug} label={EMP_LABELS[slug]} value={porEmp[slug] || 0} max={max} />;
            })}
          </div>
        </div>
        <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
          <h3 className="text-sm font-bold text-[color:var(--torres-ink)]">Por classe de qualificação</h3>
          <div className="mt-4 grid grid-cols-4 gap-3">
            {["A", "B", "C", "D"].map((c) => (
              <div key={c} className="rounded-xl border border-[color:var(--torres-line)] p-3 text-center">
                <div
                  className="mx-auto flex h-8 w-8 items-center justify-center rounded-full text-sm font-extrabold text-white"
                  style={{ background: CLASSE_COLORS[c] }}
                >
                  {c}
                </div>
                <div className="mt-2 text-xl font-extrabold text-[color:var(--torres-ink)]">
                  {classes[c] || 0}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
