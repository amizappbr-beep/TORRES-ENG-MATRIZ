import React from "react";
import { Link } from "react-router-dom";
import { MessageCircle } from "lucide-react";

export const NAVY = "#0B2A4A";

export function TorresLogo({ light = false }) {
  return (
    <Link to="/" className="flex items-center gap-2 no-underline">
      <div
        className="flex h-9 w-9 items-center justify-center rounded-lg font-black"
        style={{
          background: light ? "#ffffff" : NAVY,
          color: light ? NAVY : "#ffffff",
        }}
      >
        T
      </div>
      <div className="leading-tight">
        <div
          className="text-[15px] font-extrabold tracking-tight"
          style={{ color: light ? "#fff" : NAVY }}
        >
          TORRES
        </div>
        <div
          className="text-[10px] font-medium uppercase tracking-[0.18em]"
          style={{ color: light ? "rgba(255,255,255,.75)" : "#6C7189" }}
        >
          Engenharia
        </div>
      </div>
    </Link>
  );
}

export function WhatsappFab({ phone = "5527998336937" }) {
  const href = `https://wa.me/${phone}?text=${encodeURIComponent(
    "Olá! Vim pelo site do Feirão Torres Engenharia e gostaria de mais informações."
  )}`;
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      data-testid="whatsapp-fab"
      className="fixed bottom-5 right-5 z-50 flex items-center gap-2 rounded-full bg-[#25D366] px-4 py-3 font-semibold text-white shadow-lg transition hover:brightness-95"
    >
      <MessageCircle className="h-5 w-5" />
      <span className="hidden sm:inline">WhatsApp</span>
    </a>
  );
}

export default function FeiraoLayout({ children, hideHeader = false }) {
  return (
    <div className="min-h-screen bg-white text-[#1B1F2E]">
      {!hideHeader && (
        <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
            <TorresLogo />
            <Link
              to="/quiz"
              data-testid="header-cta"
              className="rounded-full px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:opacity-90"
              style={{ background: NAVY }}
            >
              Fazer minha análise
            </Link>
          </div>
        </header>
      )}
      <main>{children}</main>
      <footer className="mt-16 border-t border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-6xl px-4 py-10 text-sm text-slate-600">
          <TorresLogo />
          <p className="mt-4 max-w-lg">
            Feirão do Imóvel Torres Engenharia — 19 de setembro de 2026.
            Residencial Reserva (Reserva 025), Rua Terezina, 25, Alterosas,
            Serra - ES.
          </p>
          <p className="mt-3 text-xs text-slate-400">
            As oportunidades apresentadas estão sujeitas à disponibilidade e a
            análise de crédito. Imagens meramente ilustrativas.
          </p>
        </div>
      </footer>
      <WhatsappFab />
    </div>
  );
}
