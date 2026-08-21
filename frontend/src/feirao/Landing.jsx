import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Home,
  Building2,
  BadgePercent,
  Users,
  Calculator,
  MapPin,
  ArrowRight,
  CheckCircle2,
  CalendarDays,
} from "lucide-react";
import FeiraoLayout, { NAVY } from "./FeiraoLayout";
import { IMAGES, EMPREENDIMENTOS } from "./data";
import { fetchConfig, track, captureUTM } from "./api";

const PORQUE = [
  {
    icon: Home,
    titulo: "Conheça uma casa pronta",
    texto: "Veja pessoalmente ambientes e dimensões de uma casa Torres.",
  },
  {
    icon: BadgePercent,
    titulo: "Condições especiais",
    texto: "Conheça oportunidades exclusivas do Feirão.",
  },
  {
    icon: Calculator,
    titulo: "Simulação",
    texto: "Entenda quais possibilidades cabem no seu orçamento.",
  },
  {
    icon: Users,
    titulo: "Atendimento direto",
    texto: "Converse diretamente com a equipe da Torres Engenharia.",
  },
  {
    icon: Building2,
    titulo: "Escolha sua oportunidade",
    texto: "Compare os empreendimentos disponíveis.",
  },
];

function Stat({ n, label }) {
  return (
    <div className="rounded-xl bg-white/10 px-4 py-3 text-center backdrop-blur">
      <div className="text-2xl font-extrabold text-white">{n}</div>
      <div className="text-xs font-medium text-white/80">{label}</div>
    </div>
  );
}

export default function Landing() {
  const [config, setConfig] = useState(null);

  useEffect(() => {
    captureUTM();
    track("page_view", { step: 0 });
    fetchConfig()
      .then(setConfig)
      .catch(() => {});
  }, []);

  const emps = config?.empreendimentos || {};
  const totalUnidades = Object.values(emps).reduce(
    (a, e) => a + (Number(e.estoque) || 0),
    0
  );
  const event = config?.event;

  return (
    <FeiraoLayout>
      {/* HERO */}
      <section className="relative overflow-hidden" style={{ background: NAVY }}>
        <img
          src={IMAGES.hero}
          alt=""
          className="absolute inset-0 h-full w-full object-cover opacity-25"
        />
        <div
          className="absolute inset-0"
          style={{
            background: `linear-gradient(180deg, rgba(11,42,74,.75), rgba(11,42,74,.95))`,
          }}
        />
        <div className="relative mx-auto max-w-6xl px-4 py-16 sm:py-24">
          <div className="flex flex-wrap items-center gap-2">
            <div className="inline-flex items-center gap-2 rounded-full bg-amber-400 px-3 py-1 text-xs font-bold text-[#0B2A4A]">
              <CalendarDays className="h-4 w-4" />
              {event?.data_label || "19 de setembro de 2026"}
            </div>
            <div className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold text-white">
              <MapPin className="h-3.5 w-3.5" />
              Local do Evento: {event?.local_nome || "Residencial Reserva 025"}
            </div>
          </div>
          <h1 className="mt-5 max-w-2xl text-4xl font-extrabold leading-tight text-white sm:text-5xl">
            II FEIRÃO DO IMÓVEL TORRES ENGENHARIA
          </h1>
          <p className="mt-4 max-w-xl text-lg text-white/85">
            Um dia para conhecer uma casa pronta, descobrir as melhores
            condições e encontrar a oportunidade que cabe no seu momento.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              to="/quiz"
              data-testid="hero-cta-primary"
              onClick={() => track("cta_click", { empreendimento: "hero" })}
              className="inline-flex items-center justify-center gap-2 rounded-full bg-amber-400 px-6 py-4 text-base font-bold text-[#0B2A4A] shadow-lg transition hover:brightness-95"
            >
              Descobrir qual casa combina comigo
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              to="/quiz"
              data-testid="hero-cta-secondary"
              className="inline-flex items-center justify-center rounded-full border border-white/40 px-6 py-4 text-base font-semibold text-white transition hover:bg-white/10"
            >
              Quero participar do Feirão
            </Link>
          </div>
          <div className="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-5">
            <Stat n={totalUnidades || 15} label="oportunidades" />
            <Stat n={Object.keys(emps).length || 4} label="empreendimentos" />
            <Stat n="★" label="condições especiais" />
            <Stat n="✓" label="atendimento direto" />
            <Stat n="$" label="simulação no local" />
          </div>
        </div>
      </section>

      {/* POR QUE PARTICIPAR */}
      <section className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="text-center text-2xl font-extrabold text-[#0B2A4A] sm:text-3xl">
          Por que participar?
        </h2>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {PORQUE.map((c) => (
            <div
              key={c.titulo}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div
                className="flex h-11 w-11 items-center justify-center rounded-xl"
                style={{ background: "#EAF0F7", color: NAVY }}
              >
                <c.icon className="h-5 w-5" />
              </div>
              <h3 className="mt-3 text-sm font-bold text-[#0B2A4A]">
                {c.titulo}
              </h3>
              <p className="mt-1 text-sm text-slate-600">{c.texto}</p>
            </div>
          ))}
        </div>
      </section>

      {/* EMPREENDIMENTOS */}
      <section className="bg-slate-50 py-14">
        <div className="mx-auto max-w-6xl px-4">
          <h2 className="text-2xl font-extrabold text-[#0B2A4A] sm:text-3xl">
            Empreendimentos no Feirão
          </h2>
          <p className="mt-2 text-slate-600">
            Escolha a oportunidade que combina com o seu momento.
          </p>
          <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {Object.values(EMPREENDIMENTOS).map((e) => {
              const estoque = emps[e.slug]?.estoque;
              const ultima = emps[e.slug]?.ultima_unidade;
              const precoLabel = emps[e.slug]?.preco_label;
              const entradaLabel = emps[e.slug]?.entrada_label;
              const statusLabel = emps[e.slug]?.status_label;
              return (
                <Link
                  key={e.slug}
                  to={`/${e.slug}`}
                  data-testid={`emp-card-${e.slug}`}
                  className="group overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md"
                >
                  <div className="relative h-40 w-full overflow-hidden">
                    <img
                      src={e.cover}
                      alt={e.nome}
                      className="h-full w-full object-cover transition group-hover:scale-105"
                    />
                    {statusLabel ? (
                      <span className="absolute left-3 top-3 rounded-full bg-green-500 px-2 py-1 text-[11px] font-bold text-white">
                        {statusLabel}
                      </span>
                    ) : ultima ? (
                      <span className="absolute left-3 top-3 rounded-full bg-amber-400 px-2 py-1 text-[11px] font-bold text-[#0B2A4A]">
                        ÚLTIMA UNIDADE
                      </span>
                    ) : null}
                  </div>
                  <div className="p-4">
                    <div className="flex items-center gap-1 text-xs text-slate-500">
                      <MapPin className="h-3.5 w-3.5" /> {e.regiao}
                    </div>
                    <h3 className="mt-1 text-base font-bold text-[#0B2A4A]">
                      {e.nome}
                    </h3>
                    {precoLabel && (
                      <p className="mt-1 text-lg font-extrabold text-[#0B2A4A]">
                        {precoLabel}
                      </p>
                    )}
                    {entradaLabel && (
                      <p className="text-xs font-semibold text-amber-600">
                        Entrada: {entradaLabel}
                      </p>
                    )}
                    {estoque != null && (
                      <div className="mt-3 inline-flex items-center gap-1 rounded-full bg-[#EAF0F7] px-2.5 py-1 text-xs font-semibold text-[#0B2A4A]">
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        {estoque} {estoque === 1 ? "unidade" : "unidades"}
                      </div>
                    )}
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA FINAL */}
      <section className="mx-auto max-w-6xl px-4 py-16">
        <div
          className="overflow-hidden rounded-3xl px-6 py-12 text-center sm:px-12"
          style={{ background: NAVY }}
        >
          <h2 className="text-2xl font-extrabold text-white sm:text-3xl">
            Vamos descobrir qual oportunidade faz sentido para você?
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-white/80">
            Responda algumas perguntas rápidas e receba uma recomendação
            personalizada — sem compromisso.
          </p>
          <Link
            to="/quiz"
            data-testid="footer-cta"
            className="mt-6 inline-flex items-center gap-2 rounded-full bg-amber-400 px-8 py-4 text-base font-bold text-[#0B2A4A] shadow-lg transition hover:brightness-95"
          >
            Fazer minha análise
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>
    </FeiraoLayout>
  );
}
