# supabase-zapi-whatsapp

Script Python que lê contatos do Supabase e envia mensagens personalizadas via WhatsApp via Z-API.

## Pré-requisitos

- Python 3.8+
- Conta no [Supabase](https://supabase.com)
- Conta na [Z-API](https://www.z-api.io) com WhatsApp conectado

## Setup da tabela

No Supabase, crie uma tabela chamada `contatos` com as colunas:

| Coluna | Tipo |
|---|---|
| `nome` | `text` |
| `telefone` | `text` (formato: `5511999999999`) |

Em **Authentication → Policies**, crie uma policy `SELECT` com `USING: true` para permitir leitura.

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```env
SUPABASE_URL=        # URL do projeto Supabase
SUPABASE_KEY=        # Publishable key do Supabase
ZAPI_INSTANCE_ID=    # ID da instância Z-API
ZAPI_TOKEN=          # Token da instância Z-API
ZAPI_CLIENT_TOKEN=   # Client-Token da conta Z-API
```

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```