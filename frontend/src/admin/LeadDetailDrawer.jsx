import React, { useEffect, useState } from "react";
import { useAdmin } from "./AdminContext";
import {
  KANBAN_COLUMNS,
  TEMP_LABEL,
  CASA_LABEL,
  MODULO_LABEL,
  formatBRL,
  formatDate,
} from "./constants";
import {
  X,
  Phone,
  Mail,
  Loader2,
  MessageCircle,
  Send,
  Flame,
  Calendar,
  Zap,
  Calculator,
  Home as HomeIcon,
  Clock,
  User,
  Bell,
  Sparkles,
} from "lucide-react";

const FAIXA_LABEL = {
  "300k": "Até R$ 300 mil",
  "350k": "R$ 350 mil",
  "400k": "R$ 400 mil",
  "450k": "R$ 450 mil",
  "500k": "R$ 500 mil+",
};
const MOMENTO_LABEL = {
  "0-3m": "Próximos 3 meses",
  "3-6m": "3 a 6 meses",
  "6-12m": "6 a 12 meses",
  "12m+": "Mais de 1 ano",
  sem_pressa: "Sem pressa",
};
const TIPO_LABEL = {
  casa: "Casa",
  apartamento: "Apartamento",
  qualquer: "Tanto faz",
};
const REGIAO_LABEL = {
  serra: "Serra",
  vitoria: "Vitória",
  vila_velha: "Vila Velha",
  qualquer: "Qualquer",
};

// ---- Feirão: rótulos das respostas do quiz ----
const EMP_NOME = {
  viva: "Residencial Viva",
  alameda: "Alameda 500",
  life: "Life 740",
  aldeia: "Aldeia 350",
};
const CLASSE_INFO = {
  A: { label: "Alta prioridade", desc: "Compra rápida, com entrada e renda compatíveis.", color: "#059669", bg: "#ECFDF5" },
  B: { label: "Boa oportunidade", desc: "Bom potencial; precisa de simulação/acompanhamento.", color: "#2563EB", bg: "#EFF6FF" },
  C: { label: "Nutrição", desc: "Interesse real, sem urgência. Nutrir e acompanhar.", color: "#D97706", bg: "#FFFBEB" },
  D: { label: "Descoberta", desc: "Pesquisando; sem planejamento financeiro ainda.", color: "#64748B", bg: "#F1F5F9" },
};
const QUIZ_LABELS = {
  objetivo: {
    __label: "Objetivo",
    primeira_casa: "Primeira casa",
    sair_aluguel: "Sair do aluguel",
    casa_maior: "Casa maior",
    investir: "Investir",
    pesquisando: "Apenas pesquisando",
  },
  prazo: {
    __label: "Prazo de compra",
    imediato: "Imediatamente",
    "30d": "Próximos 30 dias",
    "1_3m": "1 a 3 meses",
    "3_6m": "3 a 6 meses",
    nao_sei: "Ainda não sei",
  },
  renda_familiar: {
    __label: "Renda familiar",
    ate_3k: "Até R$ 3.000",
    "3_4.5k": "R$ 3.001 a 4.500",
    "4.5_6k": "R$ 4.501 a 6.000",
    "6_8k": "R$ 6.001 a 8.000",
    "8_12k": "R$ 8.001 a 12.000",
    acima_12k: "Acima de R$ 12.000",
  },
  composicao_renda: {
    __label: "Composição de renda",
    sozinho: "Sozinho",
    conjuge: "Cônjuge/companheiro(a)",
    familiar: "Familiar",
    nao_sei: "Ainda não sei",
  },
  tipo_renda: {
    __label: "Tipo de renda",
    clt: "CLT",
    servidor: "Servidor público",
    empresario: "Empresário",
    mei: "MEI",
    autonomo: "Autônomo",
    aposentado: "Aposentado",
    outro: "Outro",
  },
  fgts: { __label: "Possui FGTS", sim: "Sim", nao: "Não", nao_sei: "Não sei" },
  fgts_valor: {
    __label: "Valor do FGTS",
    ate_10k: "Até R$ 10 mil",
    "10_30k": "R$ 10 a 30 mil",
    "30_50k": "R$ 30 a 50 mil",
    mais_50k: "Mais de R$ 50 mil",
    nao_sei: "Não sei",
  },
  entrada: {
    __label: "Entrada disponível",
    sem_entrada: "Sem entrada",
    ate_10k: "Até R$ 10 mil",
    "10_30k": "R$ 10 a 30 mil",
    "30_50k": "R$ 30 a 50 mil",
    "50_100k": "R$ 50 a 100 mil",
    "100_150k": "R$ 100 a 150 mil",
    acima_150k: "Acima de R$ 150 mil",
  },
  moradia: {
    __label: "Moradia atual",
    aluguel: "Aluguel",
    familiares: "Com familiares",
    proprio: "Imóvel próprio",
    financiado: "Imóvel financiado",
    outro: "Outro",
  },
  aluguel_valor: {
    __label: "Valor do aluguel",
    ate_800: "Até R$ 800",
    "800_1200": "R$ 800 a 1.200",
    "1200_1800": "R$ 1.200 a 1.800",
    acima_1800: "Acima de R$ 1.800",
  },
  financiamento: {
    __label: "Financiamento",
    aprovado: "Já aprovado",
    nao_aprovado: "Não aprovado",
    nao_conclui: "Não concluiu",
    nunca: "Nunca fez",
  },
  financiamento_valor: {
    __label: "Valor aprovado",
    ate_150k: "Até R$ 150 mil",
    "150_250k": "R$ 150 a 250 mil",
    "250_400k": "R$ 250 a 400 mil",
    acima_400k: "Acima de R$ 400 mil",
  },
  restricao: {
    __label: "Restrição de crédito",
    nao: "Não",
    sim: "Sim",
    nao_certeza: "Não tem certeza",
  },
  regiao: {
    __label: "Região de interesse",
    jacaraipe: "Jacaraípe",
    alterosas: "Alterosas",
    serra: "Serra",
    aberto: "Aberto a regiões",
    todas: "Todas",
  },
  preferencias: {
    __label: "Preferências",
    preco: "Preço",
    entrada_facil: "Entrada facilitada",
    localizacao: "Localização",
    praia: "Proximidade da praia",
    quintal: "Quintal",
    duplex: "Casa duplex",
    ultima_unidade: "Última unidade",
    valorizacao: "Valorização",
  },
  confirmou_feirao: {
    __label: "Presença no Feirão",
    sim: "Confirmou",
    talvez: "Talvez",
    nao: "Não vai",
  },
  horario_feirao: {
    __label: "Horário preferido",
    "09_10": "09h às 10h",
    "10_11": "10h às 11h",
    "11_12": "11h às 12h",
    manha: "Manhã",
    inicio_tarde: "Início da tarde",
    final_tarde: "Final da tarde",
  },
};

function quizVal(field, value) {
  const map = QUIZ_LABELS[field];
  if (!map || value == null || value === "") return null;
  if (Array.isArray(value)) {
    const arr = value.map((v) => map[v] || v);
    return arr.length ? arr.join(", ") : null;
  }
  return map[value] || value;
}

export default function LeadDetailDrawer({ leadId, onClose, onStatusChanged, brokers = [], onOwnerChanged }) {
  const { axiosAdmin } = useAdmin();
  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);
  const [noteText, setNoteText] = useState("");
  const [savingNote, setSavingNote] = useState(false);
  const [savingStatus, setSavingStatus] = useState(false);
  const [savingOwner, setSavingOwner] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function run() {
      setLoading(true);
      try {
        const { data } = await axiosAdmin.get(`/admin/leads/${leadId}`);
        if (!cancelled) setLead(data);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    if (leadId) run();
    return () => {
      cancelled = true;
    };
  }, [leadId, axiosAdmin]);

  const updateStatus = async (next) => {
    if (!lead || next === lead.status) return;
    setSavingStatus(true);
    try {
      await axiosAdmin.patch(`/admin/leads/${lead.id}/status`, { status: next });
      setLead((l) => ({ ...l, status: next }));
      onStatusChanged?.(lead.id, next);
    } finally {
      setSavingStatus(false);
    }
  };

  const updateOwner = async (brokerId) => {
    if (!lead) return;
    if ((brokerId || null) === (lead.owner_broker_id || null)) return;
    setSavingOwner(true);
    try {
      const { data } = await axiosAdmin.patch(`/admin/leads/${lead.id}/owner`, {
        broker_id: brokerId || null,
      });
      setLead((l) => ({
        ...l,
        owner_broker_id: data.owner_broker_id,
        owner_broker_name: data.owner_broker_name,
      }));
      onOwnerChanged?.(lead.id, data.owner_broker_id, data.owner_broker_name);
    } finally {
      setSavingOwner(false);
    }
  };

  const addNote = async (e) => {
    e.preventDefault();
    if (!noteText.trim()) return;
    setSavingNote(true);
    try {
      const { data } = await axiosAdmin.post(`/admin/leads/${lead.id}/notes`, {
        text: noteText.trim(),
      });
      setLead((l) => ({ ...l, admin_notes: [...(l.admin_notes || []), data] }));
      setNoteText("");
    } finally {
      setSavingNote(false);
    }
  };

  const openWhatsapp = () => {
    if (!lead?.phone) return;
    const cleaned = lead.phone.replace(/\D/g, "");
    const withCountry = cleaned.startsWith("55") ? cleaned : `55${cleaned}`;
    const greeting = lead.name ? `Olá ${lead.name},` : "Olá,";
    const empNome = EMP_NOME[lead.empreendimento_recomendado] || "os empreendimentos do Feirão";
    const msg = `${greeting} aqui é da Torres Engenharia sobre o seu interesse no ${empNome} (II Feirão do Imóvel). Posso te ajudar?`;
    window.open(`https://wa.me/${withCountry}?text=${encodeURIComponent(msg)}`, "_blank", "noopener");
  };

  if (!leadId) return null;

  const temp = lead ? TEMP_LABEL[lead.temperatura] || TEMP_LABEL.frio : TEMP_LABEL.frio;
  const sim = lead?.simulacao;

  return (
    <>
      <div
        className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm fade-up"
        onClick={onClose}
        data-testid="lead-drawer-overlay"
      />
      <div
        className="fixed right-0 top-0 z-50 flex h-full w-full max-w-2xl flex-col overflow-hidden bg-white shadow-[-20px_0_60px_-20px_rgba(0,0,0,0.3)]"
        data-testid="lead-drawer"
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[color:var(--torres-line)] p-4">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <span className="inline-block h-2 w-2 rounded-full" style={{ backgroundColor: temp.dot }} aria-hidden />
              <div className="text-[11px] uppercase tracking-[0.22em]" style={{ color: "var(--torres-muted)" }}>
                {temp.text}
              </div>
            </div>
            <div className="serif mt-1 truncate text-xl font-semibold" style={{ color: "var(--torres-ink)" }}>
              {lead?.name || "(sem nome)"}
            </div>
            {lead?.id && (
              <div
                className="mt-0.5 inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-0.5 font-mono text-[11px] font-bold tracking-wider text-slate-600"
                data-testid="lead-drawer-codigo"
                title="Código de atendimento informado ao cliente"
              >
                Cód. {lead.id.slice(0, 8).toUpperCase()}
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            data-testid="lead-drawer-close"
            className="ml-3 flex h-9 w-9 items-center justify-center rounded-full border border-[color:var(--torres-line)] text-[color:var(--torres-muted)] transition-colors hover:border-[color:var(--torres-indigo)] hover:text-[color:var(--torres-indigo)]"
            aria-label="Fechar"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {loading || !lead ? (
          <div className="flex flex-1 items-center justify-center">
            <Loader2 className="h-6 w-6 animate-spin text-[color:var(--torres-indigo)]" />
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-5">
            {/* Contact + quick actions */}
            <div className="rounded-2xl border border-[color:var(--torres-line)] bg-[color:var(--torres-cream)] p-4">
              {lead.phone && (
                <div className="flex items-center gap-2 text-sm" style={{ color: "var(--torres-ink)" }}>
                  <Phone className="h-4 w-4" style={{ color: "var(--torres-indigo)" }} />
                  {lead.phone}
                </div>
              )}
              {lead.email && (
                <div className="mt-1 flex items-center gap-2 text-sm" style={{ color: "var(--torres-ink)" }}>
                  <Mail className="h-4 w-4" style={{ color: "var(--torres-indigo)" }} />
                  {lead.email}
                </div>
              )}
              <div className="mt-3 flex flex-wrap gap-2">
                <button
                  onClick={openWhatsapp}
                  disabled={!lead.phone}
                  data-testid="lead-drawer-whatsapp-btn"
                  className="inline-flex items-center gap-2 rounded-full bg-emerald-600 px-4 py-2 text-xs font-semibold text-white transition-all hover:bg-emerald-700 disabled:opacity-50"
                >
                  <MessageCircle className="h-3.5 w-3.5" />
                  Abrir WhatsApp
                </button>
                <div className="text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                  Criado em {formatDate(lead.created_at)}
                </div>
              </div>
            </div>

            {/* Kanban status switcher */}
            <div className="mt-5">
              <div className="mb-2 text-[11px] uppercase tracking-[0.22em]" style={{ color: "var(--torres-muted)" }}>
                Status
              </div>
              <div className="flex flex-wrap gap-1.5" data-testid="lead-drawer-status-switcher">
                {KANBAN_COLUMNS.map((col) => {
                  const Icon = col.icon;
                  const active = col.id === lead.status;
                  return (
                    <button
                      key={col.id}
                      onClick={() => updateStatus(col.id)}
                      disabled={savingStatus}
                      data-testid={`lead-drawer-status-${col.id}`}
                      className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-semibold transition-all ${
                        active ? "border-transparent text-white shadow-sm" : "bg-white hover:opacity-80"
                      }`}
                      style={
                        active
                          ? { backgroundColor: col.color }
                          : { borderColor: col.color, color: col.color }
                      }
                    >
                      <Icon className="h-3.5 w-3.5" />
                      {col.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Owner (Corretor responsável) */}
            <div className="mt-5" data-testid="lead-drawer-owner-section">
              <div className="mb-2 flex items-center justify-between">
                <div className="text-[11px] uppercase tracking-[0.22em]" style={{ color: "var(--torres-muted)" }}>
                  Corretor responsável
                </div>
                {lead.owner_broker_id && (
                  <button
                    type="button"
                    onClick={() => updateOwner(null)}
                    disabled={savingOwner}
                    data-testid="lead-drawer-owner-unassign"
                    className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 hover:text-red-600 disabled:opacity-50"
                  >
                    Remover
                  </button>
                )}
              </div>
              {brokers.length === 0 ? (
                <div
                  className="rounded-xl border border-dashed border-[color:var(--torres-line)] p-3 text-xs italic"
                  style={{ color: "var(--torres-muted)" }}
                >
                  Nenhum corretor cadastrado. Vá em "Corretores" para começar a
                  atribuir leads.
                </div>
              ) : (
                <select
                  value={lead.owner_broker_id || ""}
                  onChange={(e) => updateOwner(e.target.value || null)}
                  disabled={savingOwner}
                  data-testid="lead-drawer-owner-select"
                  className="w-full rounded-xl border border-[color:var(--torres-line)] bg-white px-3 py-2.5 text-sm outline-none transition-all focus:border-[color:var(--torres-indigo)] focus:ring-2 focus:ring-[color:var(--torres-indigo)]/15"
                >
                  <option value="">— Sem dono (pool) —</option>
                  {brokers.map((b) => (
                    <option key={b.id} value={b.id} disabled={!b.active}>
                      {b.name} {b.active ? `(${b.leads_count} leads)` : "(inativo)"}
                    </option>
                  ))}
                </select>
              )}
            </div>

            {/* Qualificação — Feirão */}
            {lead.classe ? (
              <section
                className="mt-5 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4"
                data-testid="lead-drawer-qualificacao"
              >
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" style={{ color: "var(--torres-indigo)" }} />
                  <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                    Qualificação · II Feirão
                  </div>
                </div>

                <div className="mt-3 flex items-center gap-3">
                  <span
                    className="flex h-12 w-12 items-center justify-center rounded-xl text-2xl font-extrabold"
                    style={{
                      color: (CLASSE_INFO[lead.classe] || CLASSE_INFO.D).color,
                      backgroundColor: (CLASSE_INFO[lead.classe] || CLASSE_INFO.D).bg,
                    }}
                  >
                    {lead.classe}
                  </span>
                  <div className="min-w-0">
                    <div className="text-sm font-bold" style={{ color: "var(--torres-ink)" }}>
                      Lead {lead.classe} · {(CLASSE_INFO[lead.classe] || CLASSE_INFO.D).label}
                    </div>
                    <div className="text-xs" style={{ color: "var(--torres-muted)" }}>
                      {(CLASSE_INFO[lead.classe] || CLASSE_INFO.D).desc}
                    </div>
                  </div>
                </div>

                <div className="mt-3 flex items-baseline gap-2">
                  <span className="serif text-3xl font-bold" style={{ color: "var(--torres-ink)" }}>
                    {lead.feirao_score ?? lead.lead_score}
                  </span>
                  <span className="text-sm" style={{ color: "var(--torres-muted)" }}>
                    / 100 · score de qualificação
                  </span>
                </div>
                <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[color:var(--torres-line)]">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${Math.min(100, lead.feirao_score ?? lead.lead_score)}%`,
                      backgroundColor: (CLASSE_INFO[lead.classe] || CLASSE_INFO.D).color,
                    }}
                  />
                </div>

                {/* Recomendação */}
                {lead.empreendimento_recomendado && (
                  <div className="mt-4 rounded-xl bg-[color:var(--torres-cream)] p-3">
                    <div className="text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                      Empreendimento recomendado
                    </div>
                    <div className="text-sm font-bold" style={{ color: "var(--torres-ink)" }}>
                      {EMP_NOME[lead.empreendimento_recomendado] || lead.empreendimento_recomendado}
                    </div>
                    {(lead.empreendimento_alternativas || []).length > 0 && (
                      <div className="mt-0.5 text-xs" style={{ color: "var(--torres-muted)" }}>
                        Alternativas:{" "}
                        {(lead.empreendimento_alternativas || [])
                          .map((s) => EMP_NOME[s] || s)
                          .join(" · ")}
                      </div>
                    )}
                  </div>
                )}

                {/* Sinais / critério de qualificação */}
                <div className="mt-4">
                  <div className="mb-1.5 text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                    Sinais de qualificação
                  </div>
                  <div className="flex flex-wrap gap-1.5" data-testid="lead-drawer-sinais">
                    {[
                      ["prazo", lead.prazo],
                      ["entrada", lead.entrada],
                      ["renda_familiar", lead.renda_familiar],
                      ["financiamento", lead.financiamento],
                    ].map(([field, val]) => {
                      const label = quizVal(field, val);
                      if (!label) return null;
                      return (
                        <span
                          key={field}
                          className="inline-flex items-center gap-1 rounded-full border border-[color:var(--torres-line)] bg-white px-2.5 py-1 text-[11px] font-semibold"
                          style={{ color: "var(--torres-ink)" }}
                        >
                          <span style={{ color: "var(--torres-muted)" }}>
                            {QUIZ_LABELS[field].__label}:
                          </span>
                          {label}
                        </span>
                      );
                    })}
                    {lead.confirmou_feirao && (
                      <span
                        className="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-[11px] font-bold text-white"
                        style={{
                          backgroundColor:
                            lead.confirmou_feirao === "sim"
                              ? "#059669"
                              : lead.confirmou_feirao === "talvez"
                              ? "#d97706"
                              : "#94a3b8",
                        }}
                      >
                        {quizVal("confirmou_feirao", lead.confirmou_feirao)}
                        {lead.horario_feirao ? ` · ${quizVal("horario_feirao", lead.horario_feirao)}` : ""}
                      </span>
                    )}
                  </div>
                </div>
              </section>
            ) : (
              <section className="mt-5 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4">
                <div className="flex items-center gap-2">
                  <Flame className="h-4 w-4" style={{ color: "var(--torres-indigo)" }} />
                  <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                    Engajamento
                  </div>
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="serif text-3xl font-bold" style={{ color: "var(--torres-ink)" }}>
                    {lead.lead_score}
                  </span>
                  <span className="text-sm" style={{ color: "var(--torres-muted)" }}>
                    / 150 · {temp.text}
                  </span>
                </div>
                <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[color:var(--torres-line)]">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${Math.min(100, (lead.lead_score / 150) * 100)}%`,
                      backgroundColor: temp.dot,
                    }}
                  />
                </div>
              </section>
            )}

            {/* Respostas do Quiz */}
            {lead.objetivo && (
              <section
                className="mt-4 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4"
                data-testid="lead-drawer-quiz"
              >
                <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                  Respostas do quiz
                </div>
                <div className="mt-3 grid grid-cols-1 gap-x-4 gap-y-2 sm:grid-cols-2">
                  {[
                    "objetivo",
                    "prazo",
                    "renda_familiar",
                    "composicao_renda",
                    "tipo_renda",
                    "fgts",
                    "fgts_valor",
                    "entrada",
                    "moradia",
                    "aluguel_valor",
                    "financiamento",
                    "financiamento_valor",
                    "restricao",
                    "regiao",
                    "preferencias",
                  ].map((field) => {
                    const label = quizVal(field, lead[field]);
                    if (!label) return null;
                    return (
                      <div key={field} className="flex flex-col border-b border-dashed border-[color:var(--torres-line)] pb-1.5">
                        <span className="text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                          {QUIZ_LABELS[field].__label}
                        </span>
                        <span className="text-sm font-medium" style={{ color: "var(--torres-ink)" }}>
                          {label}
                        </span>
                      </div>
                    );
                  })}
                  {lead.cidade && (
                    <div className="flex flex-col border-b border-dashed border-[color:var(--torres-line)] pb-1.5">
                      <span className="text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                        Cidade
                      </span>
                      <span className="text-sm font-medium" style={{ color: "var(--torres-ink)" }}>
                        {lead.cidade}
                      </span>
                    </div>
                  )}
                </div>
                {lead.utm && Object.keys(lead.utm).length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {Object.entries(lead.utm).map(([k, v]) => (
                      <span key={k} className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-600">
                        {k}: {String(v)}
                      </span>
                    ))}
                  </div>
                )}
              </section>
            )}

            {/* Journey */}
            <section className="mt-4 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4" data-testid="lead-drawer-journey">
              <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                Jornada explorada
              </div>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {(lead.modulos_visitados || []).length === 0 && (
                  <span className="text-xs italic" style={{ color: "var(--torres-muted)" }}>
                    Nenhum módulo concluído ainda.
                  </span>
                )}
                {(lead.modulos_visitados || []).map((m) => (
                  <span
                    key={m}
                    className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-2 py-1 text-[11px] font-semibold text-emerald-700"
                  >
                    {MODULO_LABEL[m] || m}
                  </span>
                ))}
              </div>
              <div className="mt-3 grid grid-cols-2 gap-3 text-xs">
                <InfoItem
                  icon={<HomeIcon className="h-3.5 w-3.5" />}
                  label="Casa preferida"
                  value={lead.casa_preferida ? CASA_LABEL[lead.casa_preferida] || lead.casa_preferida : "—"}
                />
                <InfoItem
                  icon={<Clock className="h-3.5 w-3.5" />}
                  label="Tempo na página"
                  value={`${Math.round((lead.tempo_total_segundos || 0) / 60)} min`}
                />
                <InfoItem
                  icon={<Zap className="h-3.5 w-3.5" />}
                  label="Atend. imediato"
                  value={lead.solicita_atendimento_imediato ? "Sim" : "Não"}
                />
                <InfoItem
                  icon={<Calendar className="h-3.5 w-3.5" />}
                  label="Agendamento"
                  value={
                    lead.agendamento
                      ? `${lead.agendamento.data} ${lead.agendamento.horario} · ${lead.agendamento.formato}`
                      : "—"
                  }
                />
              </div>
            </section>

            {/* Quiz answers */}
            {lead.quiz_answers?.length > 0 && (
              <section className="mt-4 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4" data-testid="lead-drawer-quiz">
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4" style={{ color: "var(--torres-indigo)" }} />
                  <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                    Quiz ({lead.quiz_answers.length} respostas)
                  </div>
                </div>
                <div className="mt-2 grid grid-cols-1 gap-1.5 text-[12px] sm:grid-cols-2">
                  {lead.quiz_answers.map((a) => (
                    <div
                      key={a.question_id}
                      className="rounded-lg border border-[color:var(--torres-line)] px-2.5 py-1.5"
                    >
                      <div className="text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                        {a.question_id}
                      </div>
                      <div style={{ color: "var(--torres-ink)" }}>{a.answer}</div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Simulation */}
            {sim?.renda_bruta > 0 && (
              <section className="mt-4 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4" data-testid="lead-drawer-simulacao">
                <div className="flex items-center gap-2">
                  <Calculator className="h-4 w-4" style={{ color: "var(--torres-indigo)" }} />
                  <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                    Simulação financeira
                  </div>
                  {sim.aprovado === true && (
                    <span className="ml-auto rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
                      PRÉ-QUALIFICADO
                    </span>
                  )}
                </div>
                <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                  <InfoItem label="Unidade" value={`Casa ${sim.unidade_numero ?? "—"}`} />
                  <InfoItem label="Renda" value={formatBRL(sim.renda_bruta)} />
                  <InfoItem label="Entrada" value={formatBRL(sim.entrada)} />
                  <InfoItem label="FGTS" value={formatBRL(sim.fgts)} />
                  <InfoItem label="Prazo" value={`${sim.prazo_meses} meses`} />
                  <InfoItem label="Faixa" value={sim.faixa_mcmv || "—"} />
                  <InfoItem label="Parcela" value={formatBRL(sim.parcela_estimada)} />
                  <InfoItem label="Financiado" value={formatBRL(sim.valor_financiado)} />
                </div>
              </section>
            )}

            {/* Lead Warehouse — sinal de nutrição */}
            {lead.nutricao_warehouse && (
              <section
                className="mt-4 rounded-2xl border-2 border-emerald-200 bg-gradient-to-br from-emerald-50 via-white to-emerald-50/40 p-4"
                data-testid="lead-drawer-warehouse"
              >
                <div className="flex items-center gap-2">
                  <Bell className="h-4 w-4 text-emerald-700" />
                  <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                    Lead Warehouse · Nutrição
                  </div>
                  <span className="ml-auto inline-flex items-center gap-1 rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
                    <Sparkles className="h-2.5 w-2.5" />
                    Aguarda lançamento
                  </span>
                </div>
                <div className="mt-3 space-y-2 text-xs">
                  {lead.nutricao_warehouse.faixas_interesse?.length > 0 && (
                    <div>
                      <div className="text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                        Faixas de interesse
                      </div>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {lead.nutricao_warehouse.faixas_interesse.map((f) => (
                          <span
                            key={f}
                            className="rounded-full bg-white px-2 py-0.5 text-[11px] font-semibold"
                            style={{ color: "var(--torres-indigo)", border: "1px solid var(--torres-line)" }}
                          >
                            {FAIXA_LABEL[f] || f}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  <div className="grid grid-cols-2 gap-2">
                    <InfoItem
                      label="Momento"
                      value={MOMENTO_LABEL[lead.nutricao_warehouse.momento_compra] || "—"}
                    />
                    <InfoItem
                      label="Tipo"
                      value={TIPO_LABEL[lead.nutricao_warehouse.tipo_preferido] || "—"}
                    />
                    <InfoItem
                      label="Região"
                      value={REGIAO_LABEL[lead.nutricao_warehouse.regiao_preferida] || lead.nutricao_warehouse.regiao_preferida || "—"}
                    />
                    <InfoItem
                      label="Origem"
                      value={lead.nutricao_warehouse.source === "obrigado" ? "Pós-jornada" : "Capa do book"}
                    />
                  </div>
                  {lead.nutricao_warehouse.observacoes && (
                    <div className="rounded-xl bg-white p-2.5 text-[12px] italic" style={{ color: "var(--torres-ink)" }}>
                      "{lead.nutricao_warehouse.observacoes}"
                    </div>
                  )}
                </div>
              </section>
            )}

            {/* Admin notes */}
            <section className="mt-4 rounded-2xl border border-[color:var(--torres-line)] bg-white p-4">
              <div className="serif text-sm font-semibold" style={{ color: "var(--torres-ink)" }}>
                Anotações do corretor
              </div>
              <div className="mt-3 space-y-2" data-testid="lead-drawer-notes-list">
                {(lead.admin_notes || []).length === 0 && (
                  <div className="text-xs italic" style={{ color: "var(--torres-muted)" }}>
                    Nenhuma anotação ainda.
                  </div>
                )}
                {(lead.admin_notes || []).map((n, idx) => (
                  <div key={idx} className="rounded-xl border border-[color:var(--torres-line)] bg-[color:var(--torres-cream)] p-3">
                    <div className="text-sm" style={{ color: "var(--torres-ink)" }}>
                      {n.text}
                    </div>
                    <div className="mt-1 text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
                      {n.author} · {formatDate(n.created_at)}
                    </div>
                  </div>
                ))}
              </div>
              <form onSubmit={addNote} className="mt-3 flex items-start gap-2" data-testid="lead-drawer-note-form">
                <textarea
                  rows={2}
                  value={noteText}
                  onChange={(e) => setNoteText(e.target.value)}
                  placeholder="Adicionar anotação…"
                  data-testid="lead-drawer-note-input"
                  className="flex-1 resize-none rounded-xl border border-[color:var(--torres-line)] bg-white px-3 py-2 text-sm outline-none transition-all focus:border-[color:var(--torres-indigo)] focus:ring-2 focus:ring-[color:var(--torres-indigo)]/15"
                />
                <button
                  type="submit"
                  disabled={!noteText.trim() || savingNote}
                  data-testid="lead-drawer-note-submit"
                  className="btn-primary-torres inline-flex items-center gap-1.5 px-4 py-2.5 text-xs disabled:opacity-50"
                >
                  {savingNote ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Send className="h-3.5 w-3.5" />}
                  Salvar
                </button>
              </form>
            </section>
          </div>
        )}
      </div>
    </>
  );
}

function InfoItem({ icon, label, value }) {
  return (
    <div className="rounded-lg border border-[color:var(--torres-line)] px-2.5 py-1.5">
      <div className="flex items-center gap-1 text-[10px] uppercase tracking-wider" style={{ color: "var(--torres-muted)" }}>
        {icon}
        {label}
      </div>
      <div className="mt-0.5 text-xs font-semibold" style={{ color: "var(--torres-ink)" }}>
        {value}
      </div>
    </div>
  );
}
