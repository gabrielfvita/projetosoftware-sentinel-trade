import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity, ArrowRight, CheckCircle2, Database, Eye, EyeOff,
  LockKeyhole, Server, ShieldCheck
} from "lucide-react";
import api from "../api/api";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function entrar(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      const response = await api.post("/auth/login", { email, senha });
      localStorage.setItem("investidor_id", response.data.investidor_id);
      navigate("/mfa");
    } catch (error) {
      setErro(error.response?.data?.detail || "Não foi possível autenticar suas credenciais.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="institutional-auth">
      <header className="auth-topbar">
        <div className="auth-topbar-brand">
          <div className="auth-logo"><Activity size={21} /></div>
          <div><strong>SentinelTrade</strong><span>Investment Operations</span></div>
        </div>
        <div className="environment-indicator"><span className="environment-dot" />Simulation Environment</div>
      </header>

      <main className="auth-workspace">
        <section className="auth-intelligence">
          <div className="intelligence-header">
            <span className="eyebrow">MARKET OVERVIEW</span>
            <h1>Controle operacional para decisões de mercado.</h1>
            <p>Execução simulada de ordens, controle de risco, carteira e auditoria em uma única plataforma.</p>
          </div>

          <div className="market-panel">
            <div className="panel-title-row">
              <div><span className="panel-kicker">MERCADO</span><strong>Ativos monitorados</strong></div>
              <span className="live-indicator"><span />SIMULATED</span>
            </div>
            <div className="market-table">
              <div className="market-table-header"><span>MÓDULO</span><span>AMBIENTE</span><span>STATUS</span></div>
              <div className="market-row"><div><strong>Ordens</strong><small>Bolsa/Corretora simulada</small></div><span>SIMULAÇÃO</span><span className="positive">OPERACIONAL</span></div>
              <div className="market-row"><div><strong>Cotações</strong><small>Provedor externo simulado</small></div><span>SIMULAÇÃO</span><span className="positive">DISPONÍVEL</span></div>
              <div className="market-row"><div><strong>Auditoria</strong><small>Registro imutável</small></div><span>ATIVO</span><span className="positive">PROTEGIDO</span></div>
            </div>
          </div>

          <div className="system-grid">
            <div className="system-item"><div className="system-icon"><Server size={18} /></div><div><span>API</span><strong><CheckCircle2 size={14} />Operacional</strong></div></div>
            <div className="system-item"><div className="system-icon"><Database size={18} /></div><div><span>Auditoria</span><strong><CheckCircle2 size={14} />Ativa</strong></div></div>
            <div className="system-item"><div className="system-icon"><ShieldCheck size={18} /></div><div><span>Segurança</span><strong><CheckCircle2 size={14} />MFA habilitado</strong></div></div>
          </div>
        </section>

        <section className="auth-access">
          <div className="access-container">
            <div className="access-header">
              <div className="access-security-icon"><LockKeyhole size={20} /></div>
              <span className="eyebrow">SECURE ACCESS</span>
              <h2>Acesso à plataforma</h2>
              <p>Utilize suas credenciais para acessar o ambiente operacional SentinelTrade.</p>
            </div>

            <form className="institutional-form" onSubmit={entrar}>
              <div className="field-group">
                <label>E-mail</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="seu@email.com" required />
              </div>
              <div className="field-group">
                <div className="field-label-row"><label>Senha</label><span>Credencial protegida</span></div>
                <div className="password-field">
                  <input type={mostrarSenha ? "text" : "password"} value={senha} onChange={(e) => setSenha(e.target.value)} placeholder="Digite sua senha" required />
                  <button type="button" className="password-toggle" onClick={() => setMostrarSenha(!mostrarSenha)}>
                    {mostrarSenha ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>
              {erro && <div className="auth-error"><span />{erro}</div>}
              <button className="institutional-submit" type="submit" disabled={carregando}>
                <span>{carregando ? "Autenticando..." : "Entrar na plataforma"}</span>
                {!carregando && <ArrowRight size={18} />}
              </button>
            </form>

            <div className="access-footer"><ShieldCheck size={16} /><p>Este acesso utiliza autenticação em duas etapas e registro de auditoria.</p></div>
          </div>
          <div className="auth-version"><span>SentinelTrade v1.0</span><span>•</span><span>Ambiente acadêmico simulado</span></div>
        </section>
      </main>
    </div>
  );
}
