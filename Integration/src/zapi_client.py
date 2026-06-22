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
        response.raise_for_status()
        logger.info(f"Mensagem enviada com sucesso para {phone}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar mensagem para {phone}: {e}")
        return False