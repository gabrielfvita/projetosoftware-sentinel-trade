export default function DataState({ loading, error, empty, children }) {
  if (loading) return <div className="state-panel">Carregando dados...</div>;
  if (error) return <div className="state-panel error-state">{error}</div>;
  if (empty) return <div className="state-panel">Nenhum registro disponível.</div>;
  return children;
}
