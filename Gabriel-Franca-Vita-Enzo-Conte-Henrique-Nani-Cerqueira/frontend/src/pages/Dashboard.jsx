import { useEffect, useMemo, useState } from "react";
import { Activity, ArrowUpRight, BriefcaseBusiness, CircleDollarSign, Gauge, ReceiptText, ShieldCheck } from "lucide-react";
import api from "../api/api";
import Layout from "../components/Layout";
import PageHeader from "../components/PageHeader";

const brl = (v) => new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(v || 0));

export default function Dashboard() {
  const [carteira, setCarteira] = useState(null);
  const [ordens, setOrdens] = useState([]);
  const [ativos, setAtivos] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/carteiras/minha"),
      api.get("/historico/minhas-ordens"),
      api.get("/ativos"),
    ])
      .then(([c, o, a]) => {
        setCarteira(c.data);
        setOrdens(Array.isArray(o.data) ? o.data : []);
        setAtivos(Array.isArray(a.data) ? a.data : []);
      })
      .catch((e) => setErro(e.response?.data?.detail || "Não foi possível carregar o dashboard."));
  }, []);

  const cotacoes = useMemo(() => {
    const mapa = {};
    ativos.forEach((ativo) => { mapa[ativo.codigo] = Number(ativo.cotacao || 0); });
    return mapa;
  }, [ativos]);

  const posicoes = useMemo(() => (
    (carteira?.posicoes || []).map((posicao) => {
      const cotacao = cotacoes[posicao.codigo_ativo] || 0;
      const quantidade = Number(posicao.quantidade || 0);
      return { ...posicao, cotacao, valor_atual: quantidade * cotacao };
    })
  ), [carteira, cotacoes]);

  const exposicao = useMemo(
    () => posicoes.reduce((soma, posicao) => soma + Number(posicao.valor_atual || 0), 0),
    [posicoes]
  );
  const saldo = Number(carteira?.saldo_disponivel ?? carteira?.saldo ?? 0);
  const limite = Number(carteira?.limite_risco ?? 0);
  const patrimonio = saldo + exposicao;
  const uso = limite > 0 ? Math.min((exposicao / limite) * 100, 100) : 0;

  return (
    <Layout>
      <PageHeader
        eyebrow="OPERATIONS OVERVIEW"
        title="Dashboard"
        description="Visão consolidada da conta, exposição e atividade operacional."
        action={<div className="market-status"><span />Mercado simulado ativo</div>}
      />

      {erro && <div className="state-panel error-state">{erro}</div>}

      <div className="terminal-stats">
        <div className="metric-block"><div className="metric-top"><span>PATRIMÔNIO ESTIMADO</span><CircleDollarSign size={16} /></div><strong>{brl(patrimonio)}</strong><small><ArrowUpRight size={13} />Saldo + posições</small></div>
        <div className="metric-block"><div className="metric-top"><span>SALDO DISPONÍVEL</span><BriefcaseBusiness size={16} /></div><strong>{brl(saldo)}</strong><small className="neutral">Liquidez imediata</small></div>
        <div className="metric-block"><div className="metric-top"><span>EXPOSIÇÃO</span><Activity size={16} /></div><strong>{brl(exposicao)}</strong><small className="neutral">Capital em posições</small></div>
        <div className="metric-block"><div className="metric-top"><span>LIMITE DE RISCO</span><Gauge size={16} /></div><strong>{brl(limite)}</strong><small className="neutral">{uso.toFixed(1)}% utilizado</small></div>
      </div>

      <div className="dashboard-grid-pro">
        <section className="terminal-panel">
          <div className="terminal-panel-head"><div><span>PORTFOLIO</span><h2>Posições abertas</h2></div><span>{posicoes.length} ativos</span></div>
          {!posicoes.length ? <div className="state-panel">Nenhuma posição em carteira.</div> : (
            <div className="table-wrapper"><table><thead><tr><th>Ativo</th><th>Qtd.</th><th>Cotação</th><th>Valor</th></tr></thead><tbody>
              {posicoes.map((posicao) => <tr key={posicao.codigo_ativo}><td><strong>{posicao.codigo_ativo}</strong></td><td>{posicao.quantidade}</td><td>{brl(posicao.cotacao)}</td><td>{brl(posicao.valor_atual)}</td></tr>)}
            </tbody></table></div>
          )}
        </section>

        <section className="terminal-panel">
          <div className="terminal-panel-head"><div><span>RISK CONTROL</span><h2>Utilização de risco</h2></div><ShieldCheck size={17} /></div>
          <div className="risk-display">
            <strong>{uso.toFixed(1)}%</strong><span>do limite disponível</span>
            <div className="risk-track"><div style={{ width: `${uso}%` }} /></div>
            <div className="risk-row"><span>Exposição</span><strong>{brl(exposicao)}</strong></div>
            <div className="risk-row"><span>Limite</span><strong>{brl(limite)}</strong></div>
          </div>
        </section>
      </div>

      <section className="terminal-panel">
        <div className="terminal-panel-head"><div><span>ORDER FLOW</span><h2>Ordens recentes</h2></div><div className="head-counter"><ReceiptText size={14} />{ordens.length} registros</div></div>
        {!ordens.length ? <div className="state-panel">Nenhuma ordem registrada.</div> : (
          <div className="table-wrapper"><table>
            <thead><tr><th>ID</th><th>Ativo</th><th>Tipo</th><th>Qtd.</th><th>Limite</th><th>Execução</th><th>Estado</th></tr></thead>
            <tbody>{ordens.slice(0, 8).map((ordem) => (
              <tr key={ordem.id_ordem ?? ordem.id}>
                <td>#{ordem.id_ordem ?? ordem.id}</td><td><strong>{ordem.codigo_ativo ?? "—"}</strong></td><td>{String(ordem.tipo ?? "—").toUpperCase()}</td><td>{ordem.quantidade ?? "—"}</td>
                <td>{brl(ordem.preco_limite ?? ordem.preco ?? 0)}</td><td>{ordem.preco_medio_execucao ? brl(ordem.preco_medio_execucao) : "—"}</td>
                <td><span className={`order-status ${ordem.estado ?? ""}`}>{String(ordem.estado ?? "—").replaceAll("_", " ")}</span></td>
              </tr>
            ))}</tbody>
          </table></div>
        )}
      </section>
    </Layout>
  );
}
