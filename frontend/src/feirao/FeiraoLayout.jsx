import React from "react";
import { Link } from "react-router-dom";
import { MessageCircle } from "lucide-react";

export const NAVY = "#0B2A4A";
const LOGO = "/logo-torres.png";

export function TorresLogo({ boxed = false, className = "" }) {
  const img = (
    <img
      src={LOGO}
      alt="Torres Engenharia"
      className={`h-6 w-auto sm:h-7 ${className}`}
    />
  );
  return (
    <Link to="/" className="inline-flex items-center no-underline">
      {boxed ? (
        <span className="flex items-center rounded-lg bg-[#0B2A4A] px-3 py-2">
          {img}
        </span>
      ) : (
        img
      )}
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
        <header
          className="sticky top-0 z-40 shadow-sm"
          style={{ background: NAVY }}
        >
          <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
            <TorresLogo />
            <Link
              to="/quiz"
              data-testid="header-cta"
              className="rounded-full bg-amber-400 px-4 py-2 text-sm font-bold text-[#0B2A4A] shadow-sm transition hover:brightness-95"
            >
              Fazer minha análise
            </Link>
          </div>
        </header>
      )}
      <main>{children}</main>
      <footer className="mt-16" style={{ background: NAVY }}>
        <div className="mx-auto max-w-6xl px-4 py-10 text-sm text-white/70">
          <TorresLogo />
          <p className="mt-4 max-w-lg">
            Feirão do Imóvel Torres Engenharia — 19 de setembro de 2026.
            Residencial Reserva (Reserva 025), Rua Terezina, 25, Alterosas,
            Serra - ES.
          </p>
          <p className="mt-3 text-xs text-white/45">
            As oportunidades apresentadas estão sujeitas à disponibilidade e a
            análise de crédito. Imagens meramente ilustrativas.
          </p>
        </div>
      </footer>
      <WhatsappFab />
    </div>
  );
}
