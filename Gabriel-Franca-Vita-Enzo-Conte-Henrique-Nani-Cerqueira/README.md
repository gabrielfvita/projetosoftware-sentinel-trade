# SentinelTrade

SentinelTrade é uma plataforma simulada de negociação de ativos financeiros desenvolvida para fins acadêmicos.

O sistema permite autenticação com segundo fator, gerenciamento e processamento de ordens de compra e venda, validações de risco, persistência relacional, auditoria de eventos e integração simulada com serviços externos.

## Tecnologias utilizadas

- Python 3.11
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- Bandit
- pip-audit
- Uvicorn

## Estrutura do projeto

```text
app/
├── api/
├── database/
├── domain/
├── integrations/
├── repositories/
├── schemas/
├── security/
├── services/
└── main.py

tests/
sql/
Docs/
```

## Funcionalidades implementadas

O backend do SentinelTrade implementa os 17 requisitos funcionais definidos na modelagem do projeto.

### Autenticação e segurança

- Login por e-mail e senha.
- Segundo fator de autenticação (MFA).
- Senhas armazenadas utilizando hash seguro.
- Limite de tentativas de autenticação.
- Mensagens genéricas para credenciais inválidas.
- Configuração sensível por variáveis de ambiente.

### Investidores

- Cadastro de investidores.
- Consulta de investidores.
- Atualização de dados cadastrais.
- Desativação de investidores.
- Validação de e-mail duplicado.

### Contas

- Criação de contas vinculadas a investidores.
- Consulta de contas.
- Listagem das contas de um investidor.
- Atualização do limite de risco.
- Bloqueio e reativação de contas.

### Carteira

- Consulta do saldo disponível.
- Consulta do limite de risco.
- Consulta da situação da conta.
- Consulta das posições de ativos.
- Atualização automática da carteira após execução de ordens.

### Ativos e cotações

- Listagem de ativos disponíveis.
- Consulta de ativo por código.
- Consulta de cotação por meio de provedor simulado.
- Validação dos dados recebidos da integração de cotações.

### Ordens

O sistema permite:

- criar ordens de compra;
- criar ordens de venda;
- consultar ordens;
- atualizar ordens;
- cancelar ordens;
- processar ordens;
- reconciliar ordens após falhas de comunicação.

Estados suportados:

- `criada`
- `validada`
- `enviada`
- `parcialmente_executada`
- `executada`
- `rejeitada`
- `cancelada`

### Regras de negócio

São realizadas validações de:

- saldo disponível;
- posição de ativos;
- limite de risco;
- situação da conta;
- situação do mercado;
- tipo da ordem;
- prevenção de duplicidade;
- transições válidas de estado.

### Execução de ordens

Quando uma ordem é executada:

- compras debitam o saldo da conta e adicionam ativos à carteira;
- vendas reduzem a posição de ativos e creditam o saldo;
- execuções parciais alteram apenas a quantidade efetivamente executada.

### Integração com bolsa simulada

- Envio de ordens para bolsa/corretora simulada.
- Execução total simulada.
- Execução parcial simulada.
- Rejeição simulada.
- Tratamento seguro de falhas de comunicação.
- Reconciliação de ordens que permaneceram no estado `enviada`.

### Histórico de operações

- Consulta do histórico de ordens por conta.
- Consulta do estado atual das ordens.
- Consulta dos eventos de auditoria associados a uma ordem.

### Notificações

- Notificação simulada de cancelamentos.
- Notificação do resultado do processamento.
- Notificação do resultado da reconciliação.

### Auditoria

Eventos relevantes são registrados no banco, incluindo:

- autenticação;
- MFA;
- criação e atualização de investidores;
- criação e alteração de contas;
- criação e validação de ordens;
- ordens duplicadas;
- envio para a bolsa;
- execução, rejeição e cancelamento;
- falhas de integração;
- reconciliação.

Os registros de auditoria são protegidos contra alteração e exclusão, garantindo sua imutabilidade.

### Persistência

O sistema utiliza banco de dados relacional SQLite com SQLAlchemy.

Principais tabelas:

- `investidores`
- `contas`
- `ativos`
- `posicoes_carteira`
- `ordens`
- `registros_auditoria`

O script SQL da estrutura está disponível em:

```text
sql/schema.sql
```

## Segurança

Foram implementadas práticas de segurança como:

- validação de entrada com Pydantic;
- allowlist para código de ativos;
- limites de tamanho e intervalo;
- consultas via SQLAlchemy;
- prevenção de SQL Injection;
- hash seguro de senhas;
- MFA;
- prevenção de duplicidade de ordens;
- ausência de segredos no código-fonte;
- configuração sensível por `.env`;
- mensagens de erro controladas;
- auditoria;
- validação de dados provenientes de integrações.

Não são utilizadas funções perigosas como `eval()`.

## Configuração

Crie e ative um ambiente virtual.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
MFA_TEST_CODE=123456
```

O arquivo `.env` não deve ser enviado ao repositório.

## Banco de dados

Para criar e popular os dados iniciais:

```powershell
python -m app.database.seed
```

Dados de teste:

```text
E-mail: gabriel@sentineltrade.com
Senha: Sentinel123
MFA: 123456
```

## Executando a aplicação

Execute:

```powershell
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

Verificação da aplicação:

```text
GET /health
```

## Principais endpoints

### Autenticação

```text
POST /auth/login
POST /auth/mfa
```

### Investidores

```text
POST  /investidores
GET   /investidores
GET   /investidores/{investidor_id}
PATCH /investidores/{investidor_id}
PATCH /investidores/{investidor_id}/desativar
```

### Contas

```text
POST  /contas
GET   /contas/{conta_id}
GET   /contas/investidor/{investidor_id}
PATCH /contas/{conta_id}
PATCH /contas/{conta_id}/bloquear
PATCH /contas/{conta_id}/ativar
```

### Carteiras

```text
GET /carteiras/{conta_id}
```

### Ativos e cotações

```text
GET /ativos
GET /ativos/{codigo}
```

### Ordens

```text
POST  /ordens
GET   /ordens/{id_ordem}
PATCH /ordens/{id_ordem}
PATCH /ordens/{id_ordem}/cancelar
POST  /ordens/{id_ordem}/processar
POST  /ordens/{id_ordem}/reconciliar
```

### Histórico e auditoria

```text
GET /historico/contas/{conta_id}/ordens
GET /historico/ordens/{ordem_id}/auditoria
```

## Testes automatizados

Execute:

```powershell
pytest -v
```

Os testes cobrem principalmente:

- criação de ordens;
- transições de estado;
- saldo insuficiente;
- limite de risco;
- posição insuficiente;
- conta bloqueada;
- entradas inválidas;
- sanitização;
- MFA.

## Análise de segurança

### Bandit

Execute:

```powershell
bandit -r app
```

Resultado esperado:

```text
No issues identified.
```

### Dependências

Execute:

```powershell
pip-audit
```

Resultado esperado:

```text
No known vulnerabilities found
```

## Documentação UML

Os diagramas UML do projeto encontram-se em:

```text
Docs/Diagramas/
```

Foram desenvolvidos:

- Casos de Uso
- Atividades
- Classes de Análise
- Classes de Projeto
- Estados
- Componentes
- Sequência

## Observação

O SentinelTrade é um sistema acadêmico e simulado.

Não realiza negociações reais, não movimenta dinheiro real e não possui integração com bolsas de valores reais.

## Ordens limitadas

O campo de preço das ordens é um **preço limite**. Compras só executam quando a cotação estiver no limite ou abaixo; vendas, no limite ou acima. Se a condição não for atendida, a ordem permanece enviada e pode ser cancelada. A execução financeira utiliza a cotação vigente e registra o preço médio executado.
