import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import MFA from "./pages/MFA";
import Dashboard from "./pages/Dashboard";
import Carteira from "./pages/Carteira";
import Ativos from "./pages/Ativos";
import Ordens from "./pages/Ordens";
import Historico from "./pages/Historico";
import Auditoria from "./pages/Auditoria";
import Contas from "./pages/Contas";
import Investidores from "./pages/Investidores";

function Protected({ children }) {
  return Boolean(localStorage.getItem("access_token"))
    ? children
    : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/mfa" element={<MFA />} />
        <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
        <Route path="/carteira" element={<Protected><Carteira /></Protected>} />
        <Route path="/ativos" element={<Protected><Ativos /></Protected>} />
        <Route path="/ordens" element={<Protected><Ordens /></Protected>} />
        <Route path="/historico" element={<Protected><Historico /></Protected>} />
        <Route path="/auditoria" element={<Protected><Auditoria /></Protected>} />
        <Route path="/contas" element={<Protected><Contas /></Protected>} />
        <Route path="/investidores" element={<Protected><Investidores /></Protected>} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
