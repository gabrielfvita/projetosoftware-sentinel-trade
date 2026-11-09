import { useEffect, useMemo, useState } from "react";
import api from "../api/api";
import Layout from "../components/Layout";
import PageHeader from "../components/PageHeader";

const brl = (v) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(v || 0));

export default function Carteira() {
  const [carteira, setCarteira] = useState(null);
  const [ativos, setAtivos] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/carteiras/minha"),
      api.get("/ativos"),
    ])
      .then(([carteiraResponse, ativosResponse]) => {
        setCarteira(carteiraResponse.data);
        setAtivos(Array.isArray(ativosResponse.data) ? ativosResponse.data : []);
      })
      .catch((error) => {
        setErro(error.response?.data?.detail || "Erro ao carregar carteira.");
      });
  }, []);

  const cotacoes = useMemo(() => {
    const mapa = {};
    ativos.forEach((ativo) => {
      mapa[ativo.codigo] = Number(ativo.cotacao || 0);
    });
    return mapa;
  }, [ativos]);

  const posicoes = carteira?.posicoes || [];
  const posicoesCalculadas = posicoes.map((posicao) => {
    const codigo = posicao.codigo_ativo;
    const cotacao = cotacoes[codigo] || 0;
    const quantidade = Number(posicao.quantidade || 0);
    return { ...posicao, cotacao, valor_atual: quantidade * cotacao };
  });

  const valorTotal = posicoesCalculadas.reduce(
    (total, posicao) => total + Number(posicao.valor_atual || 0),
    0
  );

  return (
    <Layout>
      <PageHeader
        eyebrow="PORTFOLIO"
        title="Carteira"
        description="Posições consolidadas, saldo e exposição da conta."
      />

      {erro && <div className="state-panel error-state">{erro}</div>}

      <div className="terminal-stats compact">
        <div className="metric-block">
          <div className="metric-top"><span>SALDO</span></div>
          <strong>{brl(carteira?.saldo_disponivel ?? carteira?.saldo)}</strong>
        </div>
        <div className="metric-block">
          <div className="metric-top"><span>VALOR EM POSIÇÕES</span></div>
          <strong>{brl(valorTotal)}</strong>
        </div>
        <div className="metric-block">
          <div className="metric-top"><span>LIMITE DE RISCO</span></div>
          <strong>{brl(carteira?.limite_risco)}</strong>
        </div>
        <div className="metric-block">
          <div className="metric-top"><span>POSIÇÕES</span></div>
          <strong>{posicoesCalculadas.length}</strong>
        </div>
      </div>

      <section className="terminal-panel">
        <div className="terminal-panel-head">
          <div><span>POSITIONS</span><h2>Composição da carteira</h2></div>
        </div>

        {!posicoesCalculadas.length ? (
          <div className="state-panel">Nenhuma posição.</div>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>Ativo</th><th>Quantidade</th><th>Cotação</th><th>Valor</th></tr></thead>
              <tbody>
                {posicoesCalculadas.map((posicao) => (
                  <tr key={posicao.codigo_ativo}>
                    <td><strong>{posicao.codigo_ativo}</strong></td>
                    <td>{posicao.quantidade}</td>
                    <td>{brl(posicao.cotacao)}</td>
                    <td>{brl(posicao.valor_atual)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </Layout>
  );
}
