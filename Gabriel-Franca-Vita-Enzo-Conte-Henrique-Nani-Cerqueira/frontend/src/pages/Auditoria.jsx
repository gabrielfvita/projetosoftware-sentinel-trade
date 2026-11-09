import { useState } from "react";
import api from "../api/api";
import Layout from "../components/Layout";
import PageHeader from "../components/PageHeader";

export default function Auditoria() {
  const [id, setId] = useState("2");
  const [dados, setDados] = useState([]);
  const [erro, setErro] = useState("");

  async function consultar(e) {
    e.preventDefault();
    setErro("");
    try {
      const r = await api.get(`/historico/ordens/${id}/auditoria`);
      setDados(Array.isArray(r.data) ? r.data : []);
    } catch (x) {
      setErro(x.response?.data?.detail || "Erro ao consultar auditoria.");
      setDados([]);
    }
  }

  return (
    <Layout>
      <PageHeader eyebrow="AUDIT TRAIL" title="Auditoria" description="Rastreabilidade dos eventos e mudanças de estado das ordens."/>
      <section className="terminal-panel">
        <form className="audit-search" onSubmit={consultar}>
          <label>ID da ordem<input type="number" min="1" value={id} onChange={(e)=>setId(e.target.value)} /></label>
          <button type="submit">Consultar trilha</button>
        </form>
      </section>

      {erro && <div className="state-panel error-state">{erro}</div>}

      <section className="terminal-panel">
        <div className="terminal-panel-head"><div><span>IMMUTABLE LOG</span><h2>Eventos de auditoria</h2></div></div>
        {!dados.length ? <div className="state-panel">Consulte uma ordem para visualizar seus eventos.</div> :
          <div className="timeline">
            {dados.map((d,i)=>(
              <div className="timeline-item" key={d.id??i}>
                <span className="timeline-dot"/>
                <div>
                  <strong>{d.acao??d.evento??d.tipo??"Evento"}</strong>
                  <p>{d.detalhes??d.descricao??d.resultado??"Registro de auditoria"}</p>
                  {d.criado_em && <small>{d.criado_em}</small>}
                </div>
              </div>
            ))}
          </div>}
      </section>
    </Layout>
  );
}
