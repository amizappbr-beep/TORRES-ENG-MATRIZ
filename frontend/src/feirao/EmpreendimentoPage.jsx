import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  MapPin,
  CheckCircle2,
  CalendarDays,
  MessageCircle,
} from "lucide-react";
import FeiraoLayout, { NAVY } from "./FeiraoLayout";
import { EMPREENDIMENTOS, buildWhatsappUrl } from "./data";
import { fetchConfig, track, captureUTM } from "./api";

export default function EmpreendimentoPage({ slug }) {
  const navigate = useNavigate();
  const [config, setConfig] = useState(null);
  const stat = EMPREENDIMENTOS[slug];

  useEffect(() => {
    captureUTM();
    track("page_view", { empreendimento: slug });
    fetchConfig()
      .then(setConfig)
      .catch(() => {});
  }, [slug]);

  if (!stat) {
    return (
      <FeiraoLayout>
        <div className="mx-auto max-w-2xl px-4 py-24 text-center">
          <h1 className="text-2xl font-bold text-[#0B2A4A]">
            Empreendimento não encontrado
          </h1>
          <Link to="/" className="mt-4 inline-block text-[#0B2A4A] underline">
            Voltar para o início
          </Link>
        </div>
      </FeiraoLayout>
    );
  }

  const cfg = config?.empreendimentos?.[slug] || {};
  const event = config?.event;
  const phone = event?.whatsapp || "5527998336937";
  const estoque = cfg.estoque;
  const quizHref = `/quiz?origem=${slug}`;

  return (
    <FeiraoLayout>
      {/* HERO */}
      <section className="relative" style={{ background: NAVY }}>
        <img
          src={stat.cover}
          alt={stat.nome}
          className="absolute inset-0 h-full w-full object-cover opacity-30"
        />
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(180deg, rgba(11,42,74,.65), rgba(11,42,74,.92))",
          }}
        />
        <div className="relative mx-auto max-w-5xl px-4 py-16">
          {cfg.ultima_unidade && (
            <span className="inline-block rounded-full bg-amber-400 px-3 py-1 text-xs font-bold text-[#0B2A4A]">
              ÚLTIMA UNIDADE
            </span>
          )}
          <div className="mt-3 flex items-center gap-1 text-sm text-white/80">
            <MapPin className="h-4 w-4" /> {stat.regiao}
          </div>
          <h1 className="mt-2 text-4xl font-extrabold text-white sm:text-5xl">
            {stat.nome}
          </h1>
          <p className="mt-3 max-w-xl text-lg text-white/85">{stat.tagline}</p>
          {estoque != null && (
            <div className="mt-4 inline-flex items-center gap-1 rounded-full bg-white/15 px-3 py-1.5 text-sm font-semibold text-white">
              <CheckCircle2 className="h-4 w-4" />
              {estoque} {estoque === 1 ? "unidade disponível" : "unidades disponíveis"}
            </div>
          )}
          <div className="mt-6 flex flex-col gap-3 sm:flex-row">
            <button
              onClick={() => navigate(quizHref)}
              data-testid="emp-cta-analise"
              className="inline-flex items-center justify-center gap-2 rounded-full bg-amber-400 px-6 py-4 text-base font-bold text-[#0B2A4A] shadow-lg transition hover:brightness-95"
            >
              Fazer minha análise <ArrowRight className="h-5 w-5" />
            </button>
            <button
              onClick={() => navigate(quizHref)}
              className="inline-flex items-center justify-center rounded-full border border-white/40 px-6 py-4 text-base font-semibold text-white transition hover:bg-white/10"
            >
              Participar do Feirão
            </button>
          </div>
        </div>
      </section>

      {/* DESCRIÇÃO + BENEFÍCIOS */}
      <section className="mx-auto max-w-5xl px-4 py-12">
        <p className="text-lg text-slate-700">{stat.descricao}</p>
        <div className="mt-8 grid gap-3 sm:grid-cols-2">
          {stat.beneficios.map((b) => (
            <div
              key={b}
              className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
            >
              <CheckCircle2 className="h-5 w-5 flex-shrink-0 text-[#0B2A4A]" />
              <span className="text-sm font-medium text-slate-700">{b}</span>
            </div>
          ))}
        </div>
        <div className="mt-8 grid gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600 sm:grid-cols-2">
          <div>
            <div className="font-semibold text-slate-500">Preço</div>
            <div>{cfg.preco_label || "A DEFINIR / CONFIGURÁVEL NO ADMIN"}</div>
          </div>
          <div>
            <div className="font-semibold text-slate-500">Entrada</div>
            <div>{cfg.entrada_label || "A DEFINIR / CONFIGURÁVEL NO ADMIN"}</div>
          </div>
        </div>
      </section>

      {/* GALERIA */}
      <section className="mx-auto max-w-5xl px-4 pb-12">
        {stat.video && (
          <video
            src={stat.video}
            poster={stat.cover}
            controls
            playsInline
            preload="metadata"
            data-testid="emp-video"
            className="mb-3 h-auto w-full rounded-2xl bg-black shadow-sm"
          />
        )}
        <div className="grid gap-3 sm:grid-cols-3">
          {stat.galeria.map((g, i) => (
            <img
              key={i}
              src={g}
              alt={`${stat.nome} ${i + 1}`}
              className="h-48 w-full rounded-2xl object-cover shadow-sm"
            />
          ))}
        </div>
      </section>

      {/* LOCALIZAÇÃO / EVENTO */}
      <section className="mx-auto max-w-5xl px-4 pb-16">
        <div
          className="flex flex-col items-start gap-4 rounded-3xl px-6 py-10 sm:flex-row sm:items-center sm:justify-between"
          style={{ background: NAVY }}
        >
          <div>
            <div className="flex items-center gap-2 text-white">
              <CalendarDays className="h-5 w-5" />
              <span className="font-bold">
                {event?.data_label || "19 de setembro de 2026"}
              </span>
            </div>
            <p className="mt-1 text-sm text-white/80">
              {event?.local_nome} — {event?.endereco}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate(quizHref)}
              className="rounded-full bg-amber-400 px-6 py-3 text-sm font-bold text-[#0B2A4A]"
            >
              Agendar visita
            </button>
            <a
              href={buildWhatsappUrl({ phone, empreendimentoNome: stat.nome })}
              target="_blank"
              rel="noreferrer"
              onClick={() =>
                track("whatsapp_clicked", { empreendimento: slug })
              }
              className="inline-flex items-center gap-2 rounded-full bg-[#25D366] px-5 py-3 text-sm font-bold text-white"
            >
              <MessageCircle className="h-4 w-4" /> Falar com a Torres
            </a>
          </div>
        </div>
      </section>
    </FeiraoLayout>
  );
}
