import logging
from src.supabase_client import fetch_contacts
from src.zapi_client import send_whatsapp_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s %(message)s]",
    handlers=[logging.StreamHandler()]
)

def main():
    logging.info("Iniciado processo de envio de mensagens...")
    # Busca os contatos no banco com limite de 3 (TESTAR)
    contacts = fetch_contacts(limit=3)

    if not contacts:
        logging.warning("Nenhum contato encontrado ou erro na busca.")
        return

    logging.info(f"Encontrado(s) {len(contacts)} contatos para processar")

    for contact in contacts:
        try:
            # Personalize a mensagem conforme o desafio
            message = f"Olá, {contact['name']} tudo bem com você?"

            success = send_whatsapp_message(contact['phone'], message)

            if success:
                logging.info(f"Mensagem enviada com sucesso para {contact['name']} ({contact['phone']})")
            else:
                logging.error(f"Falha ao enviar mensagem para {contact['name']} ({contact['phone']})")

        except KeyError as e:
            logging.error(f"Contato missing required field {e}: {contact}")
        except Exception as e:
            logging.error(f"Erro inesperado ao processar contato {contact.get('name', 'unknown')}: {e}")

    logging.info("Processo de envio de mensagens concluído.")

if __name__ == "__main__":
    main()