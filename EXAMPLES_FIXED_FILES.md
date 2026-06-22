# Examples of Fixed Files

This document shows examples of how the files should look after fixing the issues identified in the code review.

## 1. Fixed Configuration File (`Integration/src/config.py`)
```python
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN]):
    raise ValueError("Erro: Variáveis de ambiente não definidas no arquivo")
```

## 2. Fixed Z-API Client (`Integration/src/zapi_client.py`)
```python
import requests
import logging
from src.config import ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN

logger = logging.getLogger(__name__)

def send_whatsapp_message(phone: str, message: str) -> bool:
    """ Envia uma mensagem de texto utilizando a API da Z-API """
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }
    
    payload = {
        "phone": phone,
        "message": message
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logger.info(f"Mensagem enviada com sucesso para {phone}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar mensagem para {phone}: {e}")
        return False
```

## 3. Main Orchestration File (`Integration/src/main.py`)
```python
import logging
from src.supabase_client import fetch_contacts
from src.zapi_client import send_whatsapp_message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to orchestrate the contact messaging process."""
    logger.info("Iniciando processo de envio de mensagens...")
    
    # Fetch contacts (limit to 3)
    contacts = fetch_contacts(limit=3)
    
    if not contacts:
        logger.warning("Nenhum contato encontrado para enviar mensagens.")
        return
    
    logger.info(f"Encontrados {len(contacts)} contatos para processar.")
    
    # Process each contact
    for contact in contacts:
        try:
            # Personalize message
            message = f"Olá, {contact['name']} tudo bem com você?"
            
            # Send message
            success = send_whatsapp_message(contact['phone'], message)
            
            if success:
                logger.info(f"Mensagem enviada com sucesso para {contact['name']} ({contact['phone']})")
            else:
                logger.error(f"Falha ao enviar mensagem para {contact['name']} ({contact['phone']})")
                
        except KeyError as e:
            logger.error(f"Contato missing required field {e}: {contact}")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar contato {contact.get('name', 'unknown')}: {e}")
    
    logger.info("Processo de envio de mensagens concluído.")

if __name__ == "__main__":
    main()
```

## 4. Updated Environment Example (`Integration/env.example`)
```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
ZAPI_INSTANCE_ID=your_zapi_instance_id_here
ZAPI_TOKEN=your_zapi_token_here
ZAPI_CLIENT_TOKEN=your_zapi_client_token_here
```

## 5. README.md Template
```markdown
# b2bflow WhatsApp Messenger

Um simples script em Python que lê contatos do Supabase e envia mensagens personalizadas via Z-API.

## Funcionalidade

- Lê até 3 contatos do banco de dados Supabase
- Personaliza a mensagem com o nome do contato: "Olá, <nome_contato> tudo bem com você?"
- Envia a mensagem via Z-API para o WhatsApp
- Limita o envio a até 3 números diferentes (ou menos, se houver menos contatos)

## Pré-requisitos

- Python 3.7+
- Conta no Supabase (plano gratuito)
- Conta na Z-API (plano gratuito)

## Configuração do Supabase

1. Crie uma tabela chamada `contacts` com a seguinte estrutura:
```sql
create table contacts (
  id uuid default uuid_generate_v4() primary key,
  name varchar(255) not null,
  phone varchar(20) not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

2. Insira alguns contatos de teste:
```sql
insert into contacts (name, phone) values
('João Silva', '+5511999999999'),
('Maria Oliveira', '+5511888888888'),
('Pedro Santos', '+5511777777777');
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
SUPABASE_URL=sua_url_do_supabase_aqui
SUPABASE_KEY=sua_chave_do_supabase_aqui
ZAPI_INSTANCE_ID=seu_id_da_instancia_zapi_aqui
ZAPI_TOKEN=seu_token_zapi_aqui
ZAPI_CLIENT_TOKEN=seu_client_token_zapi_aqui
```

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Configure o arquivo `.env` conforme descrito acima
4. Execute o script:
```bash
python src/main.py
```

## Estrutura do Projeto

```
.
├── src/
│   ├── main.py           # Script principal de orquestração
│   ├── config.py         # Configuração e variáveis de ambiente
│   ├── supabase_client.py # Cliente para interação com Supabase
│   └── zapi_client.py    # Cliente para interação com Z-API
├── requirements.txt      # Dependências do projeto
├── env.example           # Exemplo de arquivo de variáveis de ambiente
└── README.md             # Este arquivo
```

## Licença

Este projeto está licenciado sob a licença MIT.
```

## 6. Requirements.txt (already looks good, but ensuring it has what's needed)
```
# Core dependencies
supabase==2.31.0
requests==2.34.2
python-dotenv==1.2.2
```

## Como Testar

Após configurar tudo corretamente, ao executar `python src/main.py`, você deveria ver algo como:

```
INFO:src.main:Iniciando processo de envio de mensagens...
INFO:src.main:Encontrados 3 contatos para processar.
INFO:src.zapi_client:Mensagem enviada com sucesso para João Silva (+5511999999999)
INFO:src.zapi_client:Mensagem enviada com sucesso para Maria Oliveira (+5511888888888)
INFO:src.zapi_client:Mensagem enviada com sucesso para Pedro Santos (+5511777777777)
INFO:src.main:Processo de envio de mensagens concluído.
```