import logging
from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

def fetch_contacts(limit: int= 3) -> list:
    """Busca os contatos cadastrados no Supabase limitando a quantidade requisitada."""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Busca id, name, phone da tabela 'contacts' limitando a ate 3 registros
        response = supabase.table("contacts").select("id, name, phone").limit(limit).execute()
        return response.data
    except Exception as e:
        logger.error(f"Erro ao buscar dados no Supabase: {e}")
        return []