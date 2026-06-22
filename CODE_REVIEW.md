# Code Review: b2bflow Python Challenge

## Overview
This document outlines what's missing and what could be improved in the current implementation of the Python script that reads contacts from Supabase and sends WhatsApp messages via Z-API.

## Current Status
The codebase has the basic structure but contains several critical issues that prevent it from functioning correctly.

## Issues Found

### 1. Configuration File (`Integration/src/config.py`)
**Critical Issues:**
- Line 7-9: `os.gatenv` should be `os.getenv` (typo)
- Missing `ZAPI_CLIENT_TOKEN` in the configuration (referenced in zapi_client.py but not defined)
- Error message in Portuguese contains typo: "Variaveis" should be "Variáveis"

**Current Code:**
```python
SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.gatenv("supabase_key")  # Should be os.getenv
ZAPI_INSTANCE_ID = os.gatenv("zapi_instance_id")  # Should be os.getenv
ZAPI_TOKEN = os.gatenv("zapi_token")  # Should be os.getenv
```

**Should Be:**
```python
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")  # Missing

if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN]):
    raise ValueError("Erro: Variáveis de ambiente não definidas no arquivo")
```

### 2. Supabase Client (`Integration/src/supabase_client.py`)
**Status:** Mostly correct, but could be improved:
- Function correctly fetches limited contacts (id, name, phone)
- Proper error handling with logging
- Returns empty list on failure (acceptable)

**Minor Improvements:**
- Consider making the table name configurable
- Add type hints for the return value (already done)
- Consider adding a timeout parameter for the Supabase call

### 3. Z-API Client (`Integration/src/zapi_client.py`)
**Critical Issues:**
- Line 3: Imports `ZAPI_CLIENT_TOKEN` from config, but this isn't defined in config.py
- Line 9: URL is hardcoded with specific instance ID and token values instead of using environment variables
- Line 13: Uses `ZAPI_CLIENT_TOKEN` in headers, but this variable isn't properly defined
- **Major Issue:** The function is incomplete - cuts off at line 21 with the `try:` statement but no actual request sending, exception handling, or return statement

**Current Incomplete Code:**
```python
def send_whatsapp_message(phone: str, message: str) -> bool:
    """ Envia uma mensagem de texto utilizando a API da Z-API """
    url= f"https://api.z-api.io/instances/3F4DA2E66300E1693B422ECFE5F84078/token/0959126663257F0D0DE9CEFF/send-text"
    
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }
    
    payload = {
        "phone": phone,
        "message": message
    }
    
    try:
        # MISSING: Actual request sending and return statement
```

**Should Be:**
```python
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

### 4. Missing Main Orchestration File
**Critical Issue:** There is no `main.py` file that ties everything together.

**Required Functionality:**
1. Load environment variables
2. Fetch contacts from Supabase (limit 3)
3. For each contact, personalize the message: "Olá, <nome_contato> tudo bem com você?"
4. Send the message via Z-API
5. Handle success/failure logging
6. Exit gracefully

**Should Be Created as:** `Integration/src/main.py`
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
            message = f"Olá, {contact['name']}} tudo bem com você?"
            
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

### 5. Missing README.md
**Critical Issue:** No README file with setup and usage instructions.

**Should Include:**
- Project description
- Setup instructions for Supabase table
- Environment variables explanation (.env file)
- How to install dependencies
- How to run the script
- Expected behavior

### 6. Environment Configuration
**Missing:** `.env` file (should be gitignored but with an example)

**Should Contain:**
```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
ZAPI_INSTANCE_ID=your_zapi_instance_id_here
ZAPI_TOKEN=your_zapi_token_here
ZAPI_CLIENT_TOKEN=your_zapi_client_token_here
```

### 7. Supabase Table Structure
**Missing:** Instructions for setting up the Supabase table.

**Should Include:**
```sql
create table contacts (
  id uuid default uuid_generate_v4() primary key,
  name varchar(255) not null,
  phone varchar(20) not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

## Recommendations for Improvement

### 1. Code Quality
- Add type hints to all functions
- Implement proper logging throughout
- Add docstrings to all public functions
- Follow PEP 8 styling guidelines
- Add unit tests for core functions

### 2. Error Handling
- Implement retry logic for failed API calls
- Add circuit breaker pattern for external service calls
- Provide more detailed error messages for debugging
- Consider adding fallback mechanisms

### 3. Security
- Ensure .env file is properly gitignored
- Consider using a secrets manager for production
- Validate phone number formats before sending
- Sanitize input to prevent injection attacks

### 4. Configuration
- Use a configuration management library (like pydantic-settings)
- Make all parameters configurable (message template, limit, etc.)
- Add validation for required configuration values

### 5. Testing
- Add unit tests using pytest
- Add integration tests (can be run against test environments)
- Mock external services (Supabase, Z-API) in tests

### 6. Documentation
- Create comprehensive README with examples
- Add inline comments explaining complex logic
- Create API documentation if expanding to a library

## Git Practices
Based on the git status, it appears the work hasn't been committed yet. Recommendations:

1. **Initial Commit:** Commit the working structure once basic functionality is implemented
2. **Feature Branches:** Use branches for major changes or experiments
3. **Commit Messages:** Use conventional commits (feat:, fix:, docs:, etc.)
4. **Regular Commits:** Commit frequently with meaningful messages
5. **Pull Requests:** Use PRs for code review before merging to main

## Summary of Missing Files
1. `Integration/src/main.py` - Main orchestration script
2. `Integration/README.md` - Setup and usage instructions
3. `Integration/.env.example` - Example environment file (partially exists as env.example but needs updating)
4. Properly configured `.env` file (should be gitignored)

## Summary of Files Needing Fixes
1. `Integration/src/config.py` - Fix typos and add missing ZAPI_CLIENT_TOKEN
2. `Integration/src/zapi_client.py` - Complete the function, fix URL construction, add proper error handling
3. `Integration/env.example` - Update to match actual variable names used in code

## Next Steps
1. Fix the configuration file typos
2. Complete the Z-API client implementation
3. Create the main orchestration file
4. Create/update the README.md
5. Test the end-to-end flow
6. Commit the changes to git