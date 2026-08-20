import React, { useEffect, useState } from "react";
import { useAdmin } from "./AdminContext";
import { Loader2, Users2, CalendarCheck, TrendingUp } from "lucide-react";

const EMP_LABELS = {
  viva: "Residencial Viva",
  alameda: "Alameda",
  life: "Residencial Life",
  aldeia: "Residencial Aldeia",
};

const CLASSE_COLORS = {
  A: "bg-green-100 text-green-700",
  B: "bg-blue-100 text-blue-700",
  C: "bg-amber-100 text-amber-700",
  D: "bg-slate-100 text-slate-600",
};

function Stat({ label, value, sub }) {
  return (
    <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-4 shadow-sm">
      <div className="text-xs font-semibold uppercase tracking-wide text-[color:var(--torres-muted)]">
        {label}
      </div>
      <div className="mt-1 text-2xl font-extrabold text-[color:var(--torres-ink)]">
        {value}
      </div>
      {sub && <div className="text-xs text-[color:var(--torres-muted)]">{sub}</div>}
    </div>
  );
}

function FunnelBar({ label, value, max }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-[color:var(--torres-ink)]">{label}</span>
        <span className="font-bold tabular-nums text-[color:var(--torres-ink)]">
          {value}
        </span>
      </div>
      <div className="mt-1 h-2.5 w-full rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-[#0B2A4A]"
          style={{ width: `${Math.max(pct, 2)}%` }}
        />
      </div>
    </div>
  );
}

export default function FeiraoView() {
  const { axiosAdmin } = useAdmin();
  const [overview, setOverview] = useState(null);
  const [funnel, setFunnel] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    Promise.all([
      axiosAdmin.get("/admin/feirao/overview"),
      axiosAdmin.get("/admin/feirao/funnel"),
    ])
      .then(([o, f]) => {
        if (!alive) return;
        setOverview(o.data);
        setFunnel(f.data);
      })
      .catch(() => {})
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [axiosAdmin]);

  if (loading) {
    return (
      <div className="flex min-h-[300px] items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-[#0B2A4A]" />
      </div>
    );
  }

  const classes = overview?.classes || { A: 0, B: 0, C: 0, D: 0 };
  const funil = funnel?.funil || {};
  const funnelMax = Math.max(1, ...Object.values(funil));
  const porEmp = overview?.por_empreendimento || {};
  const porOrigem = funnel?.por_origem || {};

  return (
    <div
      data-testid="admin-feirao-view"
      className="mx-auto max-w-[1600px] px-6 py-6 sm:px-10"
    >
      {/* Visão geral */}
      <h2 className="flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-[color:var(--torres-muted)]">
        <TrendingUp className="h-4 w-4" /> Visão geral
      </h2>
      <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        <Stat label="Total de leads" value={overview?.total ?? 0} />
        <Stat label="Leads hoje" value={overview?.hoje ?? 0} />
        <Stat label="Inscritos no Feirão" value={overview?.inscritos_feirao ?? 0} />
        <Stat label="Confirmados" value={overview?.confirmados_feirao ?? 0} />
        <Stat
          label="Leads A + B"
          value={(classes.A || 0) + (classes.B || 0)}
          sub="alta prioridade"
        />
        <Stat label="Leads C + D" value={(classes.C || 0) + (classes.D || 0)} />
      </div>

      {/* Classificação */}
      <h2 className="mt-8 flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-[color:var(--torres-muted)]">
        <Users2 className="h-4 w-4" /> Classificação dos leads
      </h2>
      <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {["A", "B", "C", "D"].map((c) => (
          <div
            key={c}
            className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-4 shadow-sm"
          >
            <span
              className={`inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-extrabold ${CLASSE_COLORS[c]}`}
            >
              {c}
            </span>
            <div className="mt-2 text-2xl font-extrabold text-[color:var(--torres-ink)]">
              {classes[c] || 0}
            </div>
            <div className="text-xs text-[color:var(--torres-muted)]">
              {c === "A"
                ? "Alta prioridade"
                : c === "B"
                ? "Boa oportunidade"
                : c === "C"
                ? "Nutrição"
                : "Descoberta"}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        {/* Funil */}
        <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
          <h3 className="text-sm font-bold text-[color:var(--torres-ink)]">
            Funil de conversão
          </h3>
          <div className="mt-4 space-y-3">
            <FunnelBar label="Visitantes" value={funil.visitantes || 0} max={funnelMax} />
            <FunnelBar label="Iniciaram quiz" value={funil.iniciaram_quiz || 0} max={funnelMax} />
            <FunnelBar label="Finalizaram quiz" value={funil.finalizaram_quiz || 0} max={funnelMax} />
            <FunnelBar label="Cadastraram" value={funil.cadastraram || 0} max={funnelMax} />
            <FunnelBar label="Agendaram" value={funil.agendaram || 0} max={funnelMax} />
            <FunnelBar label="Clicaram no WhatsApp" value={funil.clicaram_whatsapp || 0} max={funnelMax} />
          </div>
        </div>

        {/* Distribuição por empreendimento */}
        <div className="rounded-2xl border border-[color:var(--torres-line)] bg-white p-5 shadow-sm">
          <h3 className="flex items-center gap-2 text-sm font-bold text-[color:var(--torres-ink)]">
            <CalendarCheck className="h-4 w-4" /> Distribuição por empreendimento
          </h3>
          <div className="mt-4 space-y-3">
            {Object.keys(EMP_LABELS).map((slug) => {
              const val = porEmp[slug] || 0;
              const max = Math.max(1, ...Object.values(porEmp));
              return (
                <FunnelBar
                  key={slug}
                  label={EMP_LABELS[slug]}
                  value={val}
                  max={max}
                />
              );
            })}
          </div>

          <h3 className="mt-6 text-sm font-bold text-[color:var(--torres-ink)]">
            Origem dos leads
          </h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {Object.keys(porOrigem).length === 0 && (
              <span className="text-xs text-[color:var(--torres-muted)]">
                Sem dados de origem ainda.
              </span>
            )}
            {Object.entries(porOrigem).map(([k, v]) => (
              <span
                key={k}
                className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700"
              >
                {k}: {v}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
