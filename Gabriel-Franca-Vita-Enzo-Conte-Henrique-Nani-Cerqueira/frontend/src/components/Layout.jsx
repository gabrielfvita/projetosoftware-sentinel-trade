import {
  Activity, BriefcaseBusiness, Building2, History, LayoutDashboard,
  LogOut, ReceiptText, ScanSearch, ShieldCheck, TrendingUp, UserRound
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";

export default function Layout({ children }) {
  const navigate = useNavigate();
  const itens = [
    ["Dashboard", "/dashboard", LayoutDashboard],
    ["Carteira", "/carteira", BriefcaseBusiness],
    ["Ativos", "/ativos", TrendingUp],
    ["Ordens", "/ordens", ReceiptText],
    ["Histórico", "/historico", History],
    ["Auditoria", "/auditoria", ScanSearch],
    ["Contas", "/contas", Building2],
    ["Meus dados", "/investidores", UserRound],
  ];

  function sair() {
    localStorage.clear();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-logo"><Activity size={20} /></div>
          <div>
            <strong>SentinelTrade</strong>
            <span>Investment Operations</span>
          </div>
        </div>

        <div className="sidebar-section-label">OPERATIONS</div>

        <nav className="sidebar-nav">
          {itens.map(([nome, caminho, Icon]) => (
            <NavLink
              key={caminho}
              to={caminho}
              className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
            >
              <Icon size={17} />
              <span>{nome}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-security">
            <ShieldCheck size={15} />
            <div>
              <strong>Secure session</strong>
              <span>MFA verified</span>
            </div>
          </div>
          <button className="logout-button" onClick={sair}>
            <LogOut size={17} />
            <span>Encerrar sessão</span>
          </button>
        </div>
      </aside>
      <main className="main-content">{children}</main>
    </div>
  );
}
