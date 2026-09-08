import React, { useCallback, useEffect, useState } from "react";
import { useAdmin } from "./AdminContext";
import { Loader2, RefreshCw, CalendarClock, Clock, Phone, MapPin } from "lucide-react";

const EMP = { viva: "Residencial Viva", alameda: "Alameda 500", life: "Life 740", aldeia: "Aldeia 350" };
const CLASSE_COLORS = { A: "#059669", B: "#2563EB", C: "#D97706", D: "#94A3B8" };
const SLOTS = [
  { key: "09_10", label: "09h às 10h" },
  { key: "10_11", label: "10h às 11h" },
  { key: "11_12", label: "11h às 12h" },
  { key: "sem_horario", label: "Sem horário definido" },
];

function SituacaoBadge({ v }) {
  const sim = v === "sim";
  return (
    <span
      className="rounded-full px-2 py-0.5 text-[10px] font-bold text-white"
      style={{ background: sim ? "#059669" : "#D97706" }}
    >
      {sim ? "Confirmado" : "Talvez"}
    </span>
  );
}

function SlotTable({ label, leads }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-[color:var(--torres-line)] bg-white shadow-sm">
      <div className="flex items-center justify-between bg-[#0B2A4A] px-4 py-2.5 text-white">
        <div className="flex items-center gap-2 font-bold">
          <Clock className="h-4 w-4" /> {label}
        </div>
        <span className="rounded-full bg-white/20 px-2 py-0.5 text-xs font-bold">
          {leads.length} {leads.length === 1 ? "pessoa" : "pessoas"}
        </span>
      </div>
      {leads.length === 0 ? (
        <div className="px-4 py-5 text-center text-sm text-[color:var(--torres-muted)]">
          Ninguém neste horário ainda.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-left text-[11px] uppercase text-[color:var(--torres-muted)]">
              <tr>
                <th className="px-3 py-2">Nome</th>
                <th className="px-3 py-2">WhatsApp</th>
                <th className="px-3 py-2">Classe</th>
                <th className="px-3 py-2">Empreendimento</th>
                <th className="px-3 py-2">Situação</th>
                <th className="px-3 py-2">Código</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((l) => (
                <tr key={l.id} className="border-t border-[color:var(--torres-line)]">
                  <td className="px-3 py-2 font-medium text-[color:var(--torres-ink)]">
                    {l.name || "—"}
                    {l.cidade && (
                      <span className="ml-1 inline-flex items-center gap-0.5 text-[10px] text-[color:var(--torres-muted)]">
                        <MapPin className="h-2.5 w-2.5" />{l.cidade}
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-2">
                    {l.phone ? (
                      <a
                        href={`https://wa.me/55${(l.phone || "").replace(/\D/g, "")}`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-[#0B2A4A] hover:underline"
                      >
                        <Phone className="h-3 w-3" />{l.phone}
                      </a>
                    ) : "—"}
                  </td>
                  <td className="px-3 py-2">
                    {l.classe ? (
                      <span
                        className="inline-flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-extrabold text-white"
                        style={{ background: CLASSE_COLORS[l.classe] || "#94A3B8" }}
                      >
                        {l.classe}
                      </span>
                    ) : "—"}
                  </td>
                  <td className="px-3 py-2 text-[color:var(--torres-muted)]">
                    {EMP[l.empreendimento_recomendado] || "—"}
                  </td>
                  <td className="px-3 py-2"><SituacaoBadge v={l.confirmou_feirao} /></td>
                  <td className="px-3 py-2 font-mono text-[11px] font-bold text-[color:var(--torres-muted)]">
                    {l.id ? l.id.slice(0, 8).toUpperCase() : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default function AgendaView() {
  const { axiosAdmin } = useAdmin();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(
    async (silent = false) => {
      if (silent) setRefreshing(true);
      try {
        const r = await axiosAdmin.get("/admin/feirao/agenda");
        setData(r.data);
      } catch (e) {
        if (e?.response?.status !== 401) console.error("Erro na agenda:", e);
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [axiosAdmin]
  );

  useEffect(() => {
    load();
  }, [load]);
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

  const slots = data?.slots || {};

  return (
    <div data-testid="admin-agenda-view" className="mx-auto max-w-[1600px] px-6 py-6 sm:px-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="flex items-center gap-2 text-lg font-bold text-[color:var(--torres-ink)]">
            <CalendarClock className="h-5 w-5" /> Agenda de Confirmação
          </h2>
          <p className="text-sm text-[color:var(--torres-muted)]">
            {data?.data_label} · {data?.horario_label} · {data?.local_nome}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-bold text-green-700">
            {data?.total_confirmados ?? 0} confirmados
          </span>
          <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-bold text-amber-700">
            {data?.total_talvez ?? 0} talvez
          </span>
          <button
            onClick={() => load(true)}
            className="flex items-center gap-1 rounded-full border border-[color:var(--torres-line)] bg-white px-3 py-1.5 text-xs font-semibold text-[color:var(--torres-ink)]"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} /> Atualizar
          </button>
        </div>
      </div>

      <div className="mt-5 space-y-5">
        {SLOTS.map((s) => (
          <SlotTable key={s.key} label={s.label} leads={slots[s.key] || []} />
        ))}
      </div>
    </div>
  );
}
