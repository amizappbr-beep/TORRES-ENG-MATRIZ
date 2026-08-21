import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  ArrowLeft,
  Loader2,
  CheckCircle2,
  MapPin,
  MessageCircle,
  Trophy,
  CalendarCheck,
} from "lucide-react";
import { TorresLogo, NAVY } from "./FeiraoLayout";
import { QUIZ, HORARIOS, EMPREENDIMENTOS, buildWhatsappUrl } from "./data";
import {
  api,
  track,
  captureUTM,
  getUTM,
  getSessionId,
} from "./api";

function OptionButton({ selected, onClick, children, testid }) {
  return (
    <button
      type="button"
      data-testid={testid}
      onClick={onClick}
      className={`flex w-full items-center justify-between rounded-2xl border-2 px-5 py-4 text-left text-[15px] font-medium transition ${
        selected
          ? "border-[#0B2A4A] bg-[#EAF0F7] text-[#0B2A4A]"
          : "border-slate-200 bg-white text-slate-700 hover:border-[#0B2A4A]/40 hover:bg-slate-50"
      }`}
    >
      <span>{children}</span>
      {selected && <CheckCircle2 className="h-5 w-5 text-[#0B2A4A]" />}
    </button>
  );
}

export default function Quiz() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState("quiz"); // quiz | capture | result
  const [baseIndex, setBaseIndex] = useState(0);
  const [showingFollow, setShowingFollow] = useState(false);
  const [answers, setAnswers] = useState({});
  const [config, setConfig] = useState(null);

  const [form, setForm] = useState({
    name: "",
    phone: "",
    email: "",
    cidade: "",
    lgpd: false,
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [lead, setLead] = useState(null);

  const [agend, setAgend] = useState({ confirmou: null, horario: null });
  const [agendSaved, setAgendSaved] = useState(false);

  useEffect(() => {
    captureUTM();
    track("quiz_started");
    api
      .get("/feirao/config")
      .then((r) => setConfig(r.data))
      .catch(() => {});
  }, []);

  const base = QUIZ[baseIndex];
  const screen = showingFollow && base.follow ? base.follow : base;
  const total = QUIZ.length;

  function setAnswer(id, value) {
    setAnswers((prev) => ({ ...prev, [id]: value }));
  }

  function advanceBase() {
    track("quiz_step_completed", { step: baseIndex + 1 });
    if (baseIndex + 1 < QUIZ.length) {
      setBaseIndex((i) => i + 1);
      setShowingFollow(false);
    } else {
      setPhase("capture");
    }
  }

  function handleSingle(scr, value) {
    setAnswer(scr.id, value);
    if (scr.id === base.id && base.follow && base.follow.when.includes(value)) {
      setShowingFollow(true);
    } else {
      advanceBase();
    }
  }

  function toggleMulti(scr, value) {
    setAnswers((prev) => {
      const arr = Array.isArray(prev[scr.id]) ? [...prev[scr.id]] : [];
      const idx = arr.indexOf(value);
      if (idx >= 0) {
        arr.splice(idx, 1);
      } else {
        if (scr.max && arr.length >= scr.max) return prev;
        arr.push(value);
      }
      return { ...prev, [scr.id]: arr };
    });
  }

  function goBack() {
    if (showingFollow) {
      setShowingFollow(false);
      return;
    }
    if (baseIndex > 0) {
      setBaseIndex((i) => i - 1);
      setShowingFollow(false);
    } else {
      navigate("/");
    }
  }

  async function submitCapture(e) {
    e.preventDefault();
    setError("");
    if (!form.name.trim() || !form.phone.trim()) {
      setError("Por favor, informe seu nome e WhatsApp.");
      return;
    }
    if (!form.lgpd) {
      setError("Precisamos da sua autorização para entrar em contato.");
      return;
    }
    setSubmitting(true);
    try {
      const utm = getUTM();
      const payload = {
        name: form.name.trim(),
        phone: form.phone.trim(),
        email: form.email.trim() || null,
        cidade: form.cidade.trim() || null,
        lgpd_consent: true,
        utm,
        origem: utm.origem || null,
        channel: utm.origem ? "campanha" : "direto",
        session_id: getSessionId(),
        ...answers,
      };
      const { data } = await api.post("/leads", payload);
      setLead(data);
      track("lead_created", { lead_id: data.id });
      track("quiz_completed", { lead_id: data.id });
      if (data.empreendimento_recomendado) {
        track("property_recommended", {
          lead_id: data.id,
          empreendimento: data.empreendimento_recomendado,
        });
      }
      setPhase("result");
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Não foi possível enviar. Tente novamente."
      );
    } finally {
      setSubmitting(false);
    }
  }

  async function saveAgendamento(confirmou, horario) {
    setAgend({ confirmou, horario });
    if (!lead?.id) return;
    try {
      await api.patch(`/leads/${lead.id}/agendamento`, {
        confirmou_feirao: confirmou,
        horario_feirao: horario || null,
      });
      track("event_signup", { lead_id: lead.id });
      if (confirmou === "sim") {
        track("appointment_created", { lead_id: lead.id });
        if (horario) setAgendSaved(true);
      } else {
        setAgendSaved(true);
      }
    } catch (_) {
      /* keep UX */
    }
  }

  const empData = useMemo(() => {
    const cfgEmps = config?.empreendimentos || {};
    const merge = (slug) => {
      if (!slug) return null;
      const stat = EMPREENDIMENTOS[slug] || {};
      const cfg = cfgEmps[slug] || {};
      return { slug, ...stat, ...cfg, nome: stat.nome || cfg.nome };
    };
    return {
      best: merge(lead?.empreendimento_recomendado),
      alts: (lead?.empreendimento_alternativas || []).map(merge).filter(Boolean),
    };
  }, [config, lead]);

  const phone = config?.event?.whatsapp || "5527998336937";
  const firstName = (lead?.name || "").split(" ")[0];

  // ---------------- RENDER ----------------
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-3">
          <TorresLogo boxed />
          {phase === "quiz" && (
            <span className="text-xs font-semibold text-slate-500">
              Etapa {baseIndex + 1} de {total}
            </span>
          )}
        </div>
        {phase === "quiz" && (
          <div className="h-1.5 w-full bg-slate-100">
            <div
              className="h-full transition-all"
              style={{
                width: `${((baseIndex + 1) / total) * 100}%`,
                background: NAVY,
              }}
            />
          </div>
        )}
      </header>

      <div className="mx-auto max-w-2xl px-4 py-8">
        {/* QUIZ */}
        {phase === "quiz" && (
          <div>
            <button
              onClick={goBack}
              className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-slate-500 hover:text-[#0B2A4A]"
            >
              <ArrowLeft className="h-4 w-4" /> Voltar
            </button>
            <h1 className="text-2xl font-extrabold text-[#0B2A4A]">
              {screen.titulo}
            </h1>
            {screen.ajuda && (
              <p className="mt-2 text-sm text-slate-500">{screen.ajuda}</p>
            )}

            <div className="mt-6 space-y-3">
              {screen.type === "single" &&
                screen.opcoes.map((o) => (
                  <OptionButton
                    key={o.value}
                    testid={`opt-${screen.id}-${o.value}`}
                    selected={answers[screen.id] === o.value}
                    onClick={() => handleSingle(screen, o.value)}
                  >
                    {o.label}
                  </OptionButton>
                ))}

              {screen.type === "multi" &&
                screen.opcoes.map((o) => {
                  const arr = answers[screen.id] || [];
                  return (
                    <OptionButton
                      key={o.value}
                      testid={`opt-${screen.id}-${o.value}`}
                      selected={arr.includes(o.value)}
                      onClick={() => toggleMulti(screen, o.value)}
                    >
                      {o.label}
                    </OptionButton>
                  );
                })}
            </div>

            {(screen.type === "multi" || showingFollow) && (
              <div className="mt-6 flex items-center justify-between">
                {showingFollow && (
                  <button
                    onClick={advanceBase}
                    className="text-sm font-medium text-slate-500 hover:text-[#0B2A4A]"
                  >
                    Pular
                  </button>
                )}
                <button
                  data-testid="quiz-continue"
                  onClick={() => {
                    if (
                      screen.type === "multi" &&
                      (!answers[screen.id] || answers[screen.id].length === 0)
                    ) {
                      return;
                    }
                    advanceBase();
                  }}
                  className="ml-auto inline-flex items-center gap-2 rounded-full px-6 py-3 text-sm font-bold text-white shadow-sm transition hover:opacity-90 disabled:opacity-40"
                  style={{ background: NAVY }}
                  disabled={
                    screen.type === "multi" &&
                    (!answers[screen.id] || answers[screen.id].length === 0)
                  }
                >
                  Continuar <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>
        )}

        {/* CAPTURE */}
        {phase === "capture" && (
          <form onSubmit={submitCapture} data-testid="capture-form">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h1 className="text-2xl font-extrabold text-[#0B2A4A]">
                Estamos quase lá!
              </h1>
              <p className="mt-2 text-sm text-slate-600">
                Para mostrar sua oportunidade e reservar seu atendimento no
                Feirão, precisamos de alguns dados:
              </p>
              <div className="mt-5 space-y-3">
                <input
                  data-testid="cap-name"
                  className="w-full rounded-xl border-2 border-slate-200 px-4 py-3 outline-none focus:border-[#0B2A4A]"
                  placeholder="Seu nome"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
                <input
                  data-testid="cap-phone"
                  className="w-full rounded-xl border-2 border-slate-200 px-4 py-3 outline-none focus:border-[#0B2A4A]"
                  placeholder="WhatsApp (com DDD)"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
                <input
                  data-testid="cap-email"
                  className="w-full rounded-xl border-2 border-slate-200 px-4 py-3 outline-none focus:border-[#0B2A4A]"
                  placeholder="E-mail (opcional)"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
                <input
                  data-testid="cap-cidade"
                  className="w-full rounded-xl border-2 border-slate-200 px-4 py-3 outline-none focus:border-[#0B2A4A]"
                  placeholder="Cidade onde mora"
                  value={form.cidade}
                  onChange={(e) => setForm({ ...form, cidade: e.target.value })}
                />
                <label className="flex items-start gap-2 text-xs text-slate-600">
                  <input
                    type="checkbox"
                    data-testid="cap-lgpd"
                    className="mt-0.5 h-4 w-4"
                    checked={form.lgpd}
                    onChange={(e) =>
                      setForm({ ...form, lgpd: e.target.checked })
                    }
                  />
                  Autorizo a Torres Engenharia a entrar em contato comigo sobre
                  os empreendimentos e condições apresentadas.
                </label>
              </div>
              {error && (
                <p className="mt-3 text-sm font-medium text-red-600">{error}</p>
              )}
              <button
                type="submit"
                data-testid="cap-submit"
                disabled={submitting}
                className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-full px-6 py-4 text-base font-bold text-white shadow-sm transition hover:opacity-90 disabled:opacity-50"
                style={{ background: NAVY }}
              >
                {submitting ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <>
                    Ver minha oportunidade <ArrowRight className="h-5 w-5" />
                  </>
                )}
              </button>
            </div>
          </form>
        )}

        {/* RESULT */}
        {phase === "result" && lead && (
          <div data-testid="result-screen">
            <div className="flex items-center gap-2 text-[#0B2A4A]">
              <Trophy className="h-6 w-6" />
              <span className="text-sm font-bold uppercase tracking-wide">
                Sua análise está pronta
              </span>
            </div>
            <h1 className="mt-2 text-2xl font-extrabold text-[#0B2A4A]">
              {firstName ? `${firstName}, ` : ""}encontramos oportunidades que
              podem combinar com o seu momento.
            </h1>

            {empData.best && (
              <div className="mt-5 overflow-hidden rounded-2xl border-2 border-[#0B2A4A] bg-white shadow-sm">
                <div className="relative h-44 w-full overflow-hidden">
                  <img
                    src={empData.best.cover}
                    alt={empData.best.nome}
                    className="h-full w-full object-cover"
                  />
                  <span className="absolute left-3 top-3 rounded-full bg-[#0B2A4A] px-3 py-1 text-[11px] font-bold text-white">
                    MELHOR OPÇÃO PARA VOCÊ
                  </span>
                  {empData.best.status_label ? (
                    <span className="absolute right-3 top-3 rounded-full bg-green-500 px-2 py-1 text-[11px] font-bold text-white">
                      {empData.best.status_label}
                    </span>
                  ) : empData.best.ultima_unidade ? (
                    <span className="absolute right-3 top-3 rounded-full bg-amber-400 px-2 py-1 text-[11px] font-bold text-[#0B2A4A]">
                      ÚLTIMA UNIDADE
                    </span>
                  ) : null}
                </div>
                <div className="p-5">
                  <div className="flex items-center gap-1 text-xs text-slate-500">
                    <MapPin className="h-3.5 w-3.5" /> {empData.best.regiao}
                    {empData.best.estoque != null && (
                      <>
                        {" · "}
                        {empData.best.estoque}{" "}
                        {empData.best.estoque === 1 ? "unidade" : "unidades"}
                      </>
                    )}
                  </div>
                  <h2 className="mt-1 text-xl font-extrabold text-[#0B2A4A]">
                    {empData.best.nome}
                  </h2>
                  {empData.best.preco_label && (
                    <div className="mt-2 flex flex-wrap items-baseline gap-x-3 gap-y-1">
                      <span className="text-lg font-extrabold text-[#0B2A4A]">
                        {empData.best.preco_label}
                      </span>
                      {empData.best.entrada_label && (
                        <span className="text-sm font-semibold text-amber-600">
                          Entrada: {empData.best.entrada_label}
                        </span>
                      )}
                    </div>
                  )}
                  {empData.best.obra_label && (
                    <p className="text-xs font-medium text-slate-500">
                      {empData.best.obra_label}
                    </p>
                  )}
                  <p className="mt-2 text-sm text-slate-600">
                    {empData.best.descricao}
                  </p>
                  <p className="mt-3 rounded-lg bg-slate-50 p-3 text-xs text-slate-500">
                    Pelo perfil informado, este empreendimento pode ser uma boa
                    opção para você. A aprovação definitiva depende da análise
                    financeira e de crédito.
                  </p>
                  <a
                    href={`/${empData.best.slug}`}
                    className="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-[#0B2A4A] hover:underline"
                  >
                    Conhecer o {empData.best.nome}
                    <ArrowRight className="h-4 w-4" />
                  </a>
                </div>
              </div>
            )}

            {empData.alts.length > 0 && (
              <div className="mt-5">
                <h3 className="text-sm font-bold text-slate-500">
                  Outras opções
                </h3>
                <div className="mt-3 grid gap-3 sm:grid-cols-2">
                  {empData.alts.map((a) => (
                    <a
                      key={a.slug}
                      href={`/${a.slug}`}
                      className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 shadow-sm transition hover:shadow-md"
                    >
                      <img
                        src={a.cover}
                        alt={a.nome}
                        className="h-14 w-14 rounded-lg object-cover"
                      />
                      <div>
                        <div className="text-sm font-bold text-[#0B2A4A]">
                          {a.nome}
                        </div>
                        <div className="text-xs text-slate-500">{a.regiao}</div>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* AGENDAMENTO */}
            <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-2 text-[#0B2A4A]">
                <CalendarCheck className="h-5 w-5" />
                <h3 className="text-base font-bold">
                  Você pretende participar do Feirão no dia 19/09?
                </h3>
              </div>
              <div className="mt-4 grid grid-cols-3 gap-2">
                {[
                  { v: "sim", l: "Sim" },
                  { v: "talvez", l: "Talvez" },
                  { v: "nao", l: "Não consigo" },
                ].map((o) => (
                  <button
                    key={o.v}
                    data-testid={`agend-${o.v}`}
                    onClick={() => saveAgendamento(o.v, null)}
                    className={`rounded-xl border-2 px-3 py-3 text-sm font-semibold transition ${
                      agend.confirmou === o.v
                        ? "border-[#0B2A4A] bg-[#EAF0F7] text-[#0B2A4A]"
                        : "border-slate-200 bg-white text-slate-700 hover:border-[#0B2A4A]/40"
                    }`}
                  >
                    {o.l}
                  </button>
                ))}
              </div>

              {agend.confirmou === "sim" && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-slate-600">
                    Qual horário é melhor para você?
                  </p>
                  <div className="mt-2 grid grid-cols-3 gap-2">
                    {HORARIOS.map((h) => (
                      <button
                        key={h.value}
                        data-testid={`horario-${h.value}`}
                        onClick={() => saveAgendamento("sim", h.value)}
                        className={`rounded-xl border-2 px-2 py-2 text-sm font-semibold transition ${
                          agend.horario === h.value
                            ? "border-[#0B2A4A] bg-[#EAF0F7] text-[#0B2A4A]"
                            : "border-slate-200 bg-white text-slate-700 hover:border-[#0B2A4A]/40"
                        }`}
                      >
                        {h.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {agendSaved && (
                <p className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-green-600">
                  <CheckCircle2 className="h-4 w-4" /> Presença registrada!
                </p>
              )}
            </div>

            {/* WHATSAPP CTA */}
            <div className="mt-6 space-y-3">
              <a
                href={buildWhatsappUrl({
                  phone,
                  empreendimentoNome: empData.best?.nome,
                  leadId: lead.id,
                })}
                target="_blank"
                rel="noreferrer"
                data-testid="whatsapp-cta"
                onClick={() =>
                  track("whatsapp_clicked", {
                    lead_id: lead.id,
                    empreendimento: empData.best?.slug,
                  })
                }
                className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-[#25D366] px-6 py-4 text-base font-bold text-white shadow-lg transition hover:brightness-95"
              >
                <MessageCircle className="h-5 w-5" />
                Falar agora com a Torres
              </a>
              <p className="text-center text-xs text-slate-400">
                Seu código de atendimento: {lead.id.slice(0, 8).toUpperCase()}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
