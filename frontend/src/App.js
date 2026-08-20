import React, { useEffect } from "react";
import "@/App.css";
import {
  BrowserRouter,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import { Toaster } from "sonner";
import Landing from "./feirao/Landing";
import Quiz from "./feirao/Quiz";
import EmpreendimentoPage from "./feirao/EmpreendimentoPage";
import AdminApp from "./admin/AdminApp";

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
  }, [pathname]);
  return null;
}

export default function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <ScrollToTop />
        <Toaster position="top-center" richColors />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/viva" element={<EmpreendimentoPage slug="viva" />} />
          <Route
            path="/alameda"
            element={<EmpreendimentoPage slug="alameda" />}
          />
          <Route path="/life" element={<EmpreendimentoPage slug="life" />} />
          <Route
            path="/aldeia"
            element={<EmpreendimentoPage slug="aldeia" />}
          />
          <Route path="/admin/*" element={<AdminApp />} />
          <Route path="/torres-admin/*" element={<AdminApp />} />
          <Route path="*" element={<Landing />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
