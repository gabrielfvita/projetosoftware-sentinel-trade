import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Activity, ArrowLeft, ArrowRight, KeyRound, LockKeyhole, ShieldCheck } from "lucide-react";
import api from "../api/api";

export default function MFA() {
  const navigate = useNavigate();
  const inputRef = useRef(null);
  const [codigo, setCodigo] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem("investidor_id")) return navigate("/login");
    inputRef.current?.focus();
  }, [navigate]);

  async function validar(e) {
    e.preventDefault();
    setErro("");
    if (codigo.length !== 6) return setErro("Informe o código de segurança com 6 dígitos.");
    setCarregando(true);
    try {
      const response = await api.post("/auth/mfa", {
        investidor_id: Number(localStorage.getItem("investidor_id")),
        codigo,
      });
      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("investidor_id", String(response.data.investidor_id));
      localStorage.setItem("conta_id", String(response.data.conta_id));
      navigate("/dashboard");
    } catch (error) {
      setErro(error.response?.data?.detail || "Código MFA inválido.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="mfa-page">
      <header className="auth-topbar">
        <div className="auth-topbar-brand">
          <div className="auth-logo"><Activity size={21} /></div>
          <div><strong>SentinelTrade</strong><span>Investment Operations</span></div>
        </div>
        <div className="environment-indicator"><span className="environment-dot" />Simulation Environment</div>
      </header>

      <main className="mfa-main">
        <div className="mfa-container">
          <div className="mfa-progress">
            <div className="mfa-step completed"><span>1</span><div><strong>Credenciais</strong><small>Verificadas</small></div></div>
            <div className="mfa-line" />
            <div className="mfa-step active"><span>2</span><div><strong>Segurança</strong><small>Validação MFA</small></div></div>
          </div>

          <div className="mfa-card">
            <div className="mfa-card-header">
              <div className="mfa-lock"><KeyRound size={24} /></div>
              <span className="eyebrow">SECOND FACTOR</span>
              <h1>Verificação de segurança</h1>
              <p>Insira o código de autenticação para concluir o acesso à plataforma.</p>
            </div>

            <form className="mfa-form" onSubmit={validar}>
              <label>Código de verificação</label>
              <input ref={inputRef} className="mfa-code-input" type="text" inputMode="numeric" maxLength={6}
                value={codigo} onChange={(e) => setCodigo(e.target.value.replace(/\D/g, "").slice(0, 6))} placeholder="000000" />
              <div className="mfa-code-info"><LockKeyhole size={14} />Código de uso único com 6 dígitos</div>
              {erro && <div className="auth-error"><span />{erro}</div>}
              <button className="institutional-submit" type="submit" disabled={carregando}>
                <span>{carregando ? "Validando..." : "Confirmar identidade"}</span>
                {!carregando && <ArrowRight size={18} />}
              </button>
            </form>

            <button type="button" className="mfa-back" onClick={() => { localStorage.removeItem("investidor_id"); navigate("/login"); }}>
              <ArrowLeft size={16} />Voltar ao login
            </button>

            <div className="mfa-security-footer">
              <ShieldCheck size={17} />
              <div><strong>Autenticação protegida</strong><span>A tentativa será registrada no histórico de auditoria.</span></div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
