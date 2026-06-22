import os
from dotenv import load_dotenv
from supabase import create_client, Client
import requests
import logging

# -------------------------------------------------------------------------------------------------- #

# Leitura dos dados em .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")#log de mensagenns


# Verificação de variaveis .env, se alguma faltar retorna quais estão faltando 
required_vars = {"SUPABASE_URL": SUPABASE_URL, "SUPABASE_KEY": SUPABASE_KEY, "ZAPI_INSTANCE_ID": ZAPI_INSTANCE_ID,
                 "ZAPI_TOKEN": ZAPI_TOKEN, "ZAPI_CLIENT_TOKEN": ZAPI_CLIENT_TOKEN,}

missing_vars = [name for name, value in required_vars.items() if not value]

if missing_vars:
    raise EnvironmentError(f"Variaveis de ambiente faltando no .env: {', '.join(missing_vars)}")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------------------------------------------------------- #

def buscar_contatos():
    resposta = supabase.table("contatos").select("nome, telefone").limit(3).execute() #Seleciona tabela contatos e busca os dados (limite 3 contatos)
    return resposta.data

def enviar_mensagem(telefone, nome):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }

    payload = {
        "phone": telefone,
        "message": f"Olá, {nome} tudo bem com você?"
    }

    resposta = requests.post(url, json=payload, headers=headers)

    return resposta

# -------------------------------------------------------------------------------------------------- #

def main():
    logging.info("Iniciando o processo de envio de mensagens...")

    contatos = buscar_contatos()

    if not contatos:
        logging.warning("Nenhum contato encontrado na tabela 'contatos'.")
        return
    
    logging.info(f"{len(contatos)} contato(s) encontrado(s). Iniciando envios...")

    total_sucesso = 0
    total_falha = 0

    for contato in contatos:
        nome = contato["nome"]
        telefone = contato["telefone"]

        try:
            resposta = enviar_mensagem(telefone, nome)

            if resposta.status_code == 200:
                logging.info(f"Mensagem enviada com sucesso para {nome} ({telefone}).")
                total_sucesso += 1

            else:
                logging.error(  f"Falha ao enviar para {nome} ({telefone}). " f"Status: {resposta.status_code} | Resposta: {resposta.text}")
                total_falha += 1

        except requests.exceptions.RequestException as erro:
              logging.error(f"Erro de conexão ao enviar para {nome} ({telefone}): {erro}")
              total_falha += 1

    logging.info(f"Finalizado. Sucesso: {total_sucesso} | Falhas: {total_falha}")


if __name__ == "__main__":
    main()