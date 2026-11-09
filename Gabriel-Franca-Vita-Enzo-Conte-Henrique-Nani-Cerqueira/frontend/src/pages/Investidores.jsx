import { useEffect, useState } from "react";
import api from "../api/api";
import Layout from "../components/Layout";
import PageHeader from "../components/PageHeader";

export default function Investidores(){
  const [dados,setDados]=useState(null); const [erro,setErro]=useState("");
  useEffect(()=>{api.get("/investidores/me").then(r=>setDados(r.data)).catch(x=>setErro(x.response?.data?.detail||"Erro ao carregar seus dados."))},[]);
  return <Layout><PageHeader eyebrow="INVESTOR PROFILE" title="Meus dados" description="Dados do investidor autenticado no SentinelTrade."/>
    {erro&&<div className="state-panel error-state">{erro}</div>}
    {dados&&<section className="terminal-panel account-panel"><div className="terminal-panel-head"><div><span>PROFILE</span><h2>{dados.nome}</h2></div></div><div className="summary-list"><div><span>E-mail</span><strong>{dados.email}</strong></div><div><span>Status</span><strong>{String(dados.status).toUpperCase()}</strong></div><div><span>MFA</span><strong>{dados.mfa_habilitado?"HABILITADO":"DESABILITADO"}</strong></div></div></section>}
  </Layout>;
}
