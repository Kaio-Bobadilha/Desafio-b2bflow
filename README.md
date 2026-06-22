# b2bflow WhatsApp Messenger

Um script em Python que consome contatos cadastrados no Supabase e realiza o disparo de mensagens automatizadas e personalizadas via Z-API. Desenvolvido como resolução do desafio técnico para a vaga de Estágio em Desenvolvimento Python.

## Funcionalidades

- Conexão e leitura de contatos no banco de dados Supabase.
- Personalização dinâmica de mensagens com o nome do destinatário: `"Olá, <nome_contato> tudo bem com você?"`.
- Integração e disparo de mensagens de texto via WhatsApp utilizando a Z-API.
- Limite de processamento de até 3 números por execução (conforme regra de negócio do desafio).

## Pré-requisitos

- Python 3.7+
- Conta no Supabase (Plano Gratuito)
- Conta na Z-API (Plano Gratuito / Instância de Teste)

## Configuração do Banco de Dados (Supabase)

1. Crie um novo projeto no Supabase e acesse o **SQL Editor**.
2. Crie uma tabela chamada `contacts` executando o seguinte script:

```sql
create table contacts (
  id uuid default uuid_generate_v4() primary key,
  name varchar(255) not null,
  phone varchar(20) not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

### Insira contatos para teste

```sql
insert into contacts (name, phone) values
('João Silva', '+5511999999999'),
('Wally Viana', '+5545999292970'),
('Kaio Quevedo', '+5545988034879');

### Variáveis de Ambiente
Crie um arquivo `.env` dentro da pasta `Integration/` (use o `env.example` como base) e preencha com as suas credenciais:

```
SUPABASE_URL=sua_url_do_supabase_aqui
SUPABASE_KEY=sua_chave_secreta_do_supabase_aqui
ZAPI_INSTANCE_ID=seu_id_da_instancia_zapi_aqui
ZAPI_TOKEN=seu_token_zapi_aqui
ZAPI_CLIENT_TOKEN=seu_client_token_zapi_aqui
```

## Instalação e Execução

Clone este repositório:
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

Instale as dependências requeridas:
```bash
pip install -r requirements.txt
```

Execute o script:
```bash
python -m src.main
```

## Estrutura do Projeto:
.
├── src/
│   ├── main.py            # Ponto de entrada e orquestração do fluxo
│   ├── config.py          # Validação e carregamento de variáveis de ambiente
│   ├── supabase_client.py # Módulo de conexão e busca de dados (Supabase)
│   └── zapi_client.py     # Módulo de requisições HTTP para envio (Z-API)
├── .env.example           # Template de variáveis de ambiente
├── .gitignore             # Arquivos e pastas ignorados pelo Git
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto