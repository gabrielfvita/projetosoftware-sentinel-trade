import { useEffect, useState } from "react";

import api from "../api/api";
import Layout from "../components/Layout";
import PageHeader from "../components/PageHeader";

const brl = (valor) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(valor || 0));

function extrairErro(error) {
  const data = error.response?.data;

  console.error("Erro ao enviar ordem:", {
    status: error.response?.status,
    data,
    message: error.message,
  });

  if (!error.response) {
    return `Erro de conexão: ${error.message}`;
  }

  if (!data) {
    return `Erro HTTP ${error.response.status}`;
  }

  if (typeof data === "string") {
    return data;
  }

  const detail = data.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const campo = Array.isArray(item.loc)
          ? item.loc[item.loc.length - 1]
          : "";

        const mensagem =
          item.msg || "Erro de validação";

        return campo
          ? `${campo}: ${mensagem}`
          : mensagem;
      })
      .join(" | ");
  }

  if (detail && typeof detail === "object") {
    return JSON.stringify(detail);
  }

  return `Erro HTTP ${error.response.status}`;
}

export default function Ordens() {
  const [ordens, setOrdens] = useState([]);

  const [erro, setErro] = useState("");
  const [cotacaoAtual, setCotacaoAtual] = useState(0);
  const [sucesso, setSucesso] = useState("");
  const [enviando, setEnviando] =
    useState(false);

  const [form, setForm] = useState({
    conta_id: Number(localStorage.getItem("conta_id") || 0),
    codigo_ativo: "PETR4",
    tipo: "compra",
    quantidade: 1,
    preco: 38.5,
    chave_idempotencia: "",
  });

  async function carregarOrdens() {
    try {
      const response = await api.get(
        "/historico/minhas-ordens"
      );

      setOrdens(
        Array.isArray(response.data)
          ? response.data
          : []
      );
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  useEffect(() => {
    carregarOrdens();
  }, []);

  useEffect(() => {
    const codigo = form.codigo_ativo.trim().toUpperCase();
    if (!/^[A-Z]{4}[0-9]{1,2}$/.test(codigo)) return;
    api.get(`/ativos/${codigo}`).then((response) => {
      const cotacao = Number(response.data?.cotacao || 0);
      setCotacaoAtual(cotacao);
      if (cotacao > 0) {
        setForm((anterior) => ({ ...anterior, preco: cotacao }));
      }
    }).catch(() => setCotacaoAtual(0));
  }, [form.codigo_ativo]);


  async function cancelarOrdem(id) {
    setErro("");
    setSucesso("");
    try {
      await api.patch(`/ordens/${id}/cancelar`);
      setSucesso(`Ordem ${id} cancelada com sucesso.`);
      await carregarOrdens();
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  async function criarOrdem(event) {
    event.preventDefault();

    setErro("");
    setSucesso("");
    setEnviando(true);

    try {
      const chave =
        form.chave_idempotencia.trim() ||
        `web_${Date.now()}`;

      const payload = {
        conta_id: Number(form.conta_id),
        codigo_ativo:
          form.codigo_ativo
            .trim()
            .toUpperCase(),

        tipo: form.tipo,

        quantidade: Number(
          form.quantidade
        ),

        preco: Number(form.preco),

        chave_idempotencia: chave,
      };

      console.log(
        "Payload enviado para /ordens:",
        payload
      );

      const response = await api.post(
        "/ordens",
        payload
      );

      console.log(
        "Resposta /ordens:",
        response.data
      );

      const id = response.data.id_ordem ?? response.data.id ?? "";
      if (response.data.estado === "enviada") {
        setSucesso(`Ordem ${id} enviada e aguardando a condição do preço limite.`);
      } else {
        setSucesso(`Ordem ${id} registrada com sucesso. Estado: ${String(response.data.estado).replaceAll("_", " ")}.`);
      }

      setForm((anterior) => ({
        ...anterior,
        chave_idempotencia: "",
      }));

      await carregarOrdens();
    } catch (error) {
      setErro(extrairErro(error));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <Layout>
      <PageHeader
        eyebrow="ORDER MANAGEMENT"
        title="Ordens"
        description="Envio, acompanhamento e controle operacional de ordens."
      />

      <div className="split-layout">
        <section className="terminal-panel">
          <div className="terminal-panel-head">
            <div>
              <span>NEW ORDER</span>
              <h2>Enviar ordem</h2>
            </div>
          </div>

          <form
            className="trade-ticket"
            onSubmit={criarOrdem}
          >
            <div className="form-row">
              <label>
                Ativo

                <input
                  type="text"
                  value={form.codigo_ativo}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      codigo_ativo:
                        event.target.value,
                    })
                  }
                  required
                />
              </label>

              <label>
                Tipo

                <select
                  value={form.tipo}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      tipo:
                        event.target.value,
                    })
                  }
                >
                  <option value="compra">
                    Compra
                  </option>

                  <option value="venda">
                    Venda
                  </option>
                </select>
              </label>
            </div>

            <div className="form-row">
              <label>
                Quantidade

                <input
                  type="number"
                  min="1"
                  value={form.quantidade}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      quantidade:
                        event.target.value,
                    })
                  }
                  required
                />
              </label>

              <label>
                Preço limite

                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={form.preco}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      preco:
                        event.target.value,
                    })
                  }
                  required
                />
                <small>Cotação atual: {brl(cotacaoAtual)}. {form.tipo === "compra" ? "A compra executa quando a cotação for menor ou igual ao limite." : "A venda executa quando a cotação for maior ou igual ao limite."}</small>
              </label>
            </div>

            <label>
              Chave de idempotência
              <small>opcional</small>

              <input
                type="text"
                value={
                  form.chave_idempotencia
                }
                onChange={(event) =>
                  setForm({
                    ...form,
                    chave_idempotencia:
                      event.target.value,
                  })
                }
                placeholder="Gerada automaticamente"
              />
            </label>

            {erro && (
              <div className="auth-error">
                <span />
                {erro}
              </div>
            )}

            {sucesso && (
              <div className="success-message">
                {sucesso}
              </div>
            )}

            <button
              className="trade-submit"
              type="submit"
              disabled={enviando}
            >
              {enviando
                ? "Transmitindo..."
                : "Transmitir ordem"}
            </button>
          </form>
        </section>

        <section className="terminal-panel">
          <div className="terminal-panel-head">
            <div>
              <span>CONTROL</span>
              <h2>Resumo</h2>
            </div>
          </div>

          <div className="summary-list">
            <div>
              <span>Total de ordens</span>
              <strong>
                {ordens.length}
              </strong>
            </div>

            <div>
              <span>Compra</span>
              <strong>
                {
                  ordens.filter(
                    (ordem) =>
                      ordem.tipo ===
                      "compra"
                  ).length
                }
              </strong>
            </div>

            <div>
              <span>Venda</span>
              <strong>
                {
                  ordens.filter(
                    (ordem) =>
                      ordem.tipo ===
                      "venda"
                  ).length
                }
              </strong>
            </div>
          </div>
        </section>
      </div>

      <section className="terminal-panel">
        <div className="terminal-panel-head">
          <div>
            <span>ORDER BOOK</span>
            <h2>
              Ordens registradas
            </h2>
          </div>

          <span>
            {ordens.length} registros
          </span>
        </div>

        {ordens.length === 0 ? (
          <div className="state-panel">
            Nenhuma ordem registrada.
          </div>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Ativo</th>
                  <th>Tipo</th>
                  <th>Qtd.</th>
                  <th>Executada</th>
                  <th>Preço limite</th>
                  <th>Preço exec.</th>
                  <th>Estado</th>
                  <th>Ação</th>
                </tr>
              </thead>

              <tbody>
                {ordens.map(
                  (ordem) => (
                    <tr
                      key={
                        ordem.id_ordem ??
                        ordem.id
                      }
                    >
                      <td>
                        #
                        {ordem.id_ordem ??
                          ordem.id}
                      </td>

                      <td>
                        <strong>
                          {
                            ordem.codigo_ativo
                          }
                        </strong>
                      </td>

                      <td>
                        {String(
                          ordem.tipo
                        ).toUpperCase()}
                      </td>

                      <td>
                        {ordem.quantidade}
                      </td>

                      <td>
                        {ordem.quantidade_executada ?? 0}
                      </td>

                      <td>{brl(ordem.preco_limite ?? ordem.preco)}</td>

                      <td>{ordem.preco_medio_execucao ? brl(ordem.preco_medio_execucao) : "—"}</td>

                      <td>
                        <span
                          className={`order-status ${
                            ordem.estado ??
                            ""
                          }`}
                        >
                          {String(
                            ordem.estado
                          ).replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </td>

                      <td>
                        {["enviada", "parcialmente_executada"].includes(ordem.estado) ? (
                          <button type="button" className="table-action" onClick={() => cancelarOrdem(ordem.id_ordem ?? ordem.id)}>
                            Cancelar
                          </button>
                        ) : "—"}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </Layout>
  );
}