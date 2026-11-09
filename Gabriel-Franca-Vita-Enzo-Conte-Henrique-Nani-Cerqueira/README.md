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

### Autenticação

- Login por e-mail e senha.
- Senhas armazenadas utilizando hash.
- Segundo fator de autenticação (MFA) controlado.
- Respostas genéricas para credenciais inválidas.
- Registro de eventos relevantes em auditoria.

### Ordens

O sistema permite:

- criar ordens;
- consultar ordens;
- atualizar ordens;
- cancelar ordens;
- processar ordens por meio de uma bolsa simulada.

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
- prevenção de duplicidade;
- transições válidas de estado.

### Carteira e saldo

Quando uma ordem é executada:

- compras debitam o saldo da conta e adicionam ativos à carteira;
- vendas reduzem a posição e creditam o saldo;
- execuções parciais alteram somente a quantidade executada.

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

### Auditoria

Eventos relevantes são registrados no banco, incluindo:

- falhas de login;
- validação de senha;
- MFA;
- criação e validação de ordens;
- duplicidade;
- envio de ordens;
- resultado da bolsa;
- cancelamento;
- atualização de ordens.

Dados sensíveis, como senha e código MFA, não são gravados nos logs de auditoria.

### Integrações simuladas

O projeto possui integrações simuladas para:

- bolsa/corretora;
- provedor de cotações;
- serviço de notificações.

As respostas externas são tratadas como dados não confiáveis e passam por validação.

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

### Ordens

```text
POST  /ordens
GET   /ordens/{id_ordem}
PATCH /ordens/{id_ordem}
PATCH /ordens/{id_ordem}/cancelar
POST  /ordens/{id_ordem}/processar
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