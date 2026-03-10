# Gest-Stock API

Flask backend project for mini-market seller registration, with local persistence (SQLite by default) and optional MySQL + Docker support.

## Overview

This API currently includes:

- Health endpoints
- Seller/user registration (`/user`)
- WhatsApp activation message integration via Twilio
- Simple layered structure (`Domain`, `Application`, `Infrastructure`, `config`)

## Tech Stack

- Python 3.8
- Flask 3
- SQLAlchemy / Flask-SQLAlchemy
- Twilio SDK
- Docker / Docker Compose (optional for MySQL and containerized app)

## Project Structure

```text
.
|-- run.py
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
`-- src/
    |-- routes.py
    |-- config/
    |   `-- data_base.py
    |-- Domain/
    |   `-- user.py
    |-- Infrastructure/
    |   `-- Model/user.py
    `-- Application/
        |-- Controllers/user_controller.py
        `-- Service/user_service.py
```

## Environment Variables (`.env`)

Create a `.env` file in the project root:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

Notes:

- These variables are required when sending WhatsApp messages.
- If missing, the app starts, but Twilio send actions return error.
- Do not commit real credentials to git.

## Database

The project is configured in `src/config/data_base.py` with two options:

1. SQLite (default)
- Active by default
- Database file: `market_management.db`
- Good for local development

2. MySQL (Docker)
- Service name in compose: `mysql57`
- Image: `mysql:8.0.29`
- Database: `market_management`
- Port mapping: `127.0.0.1:3306:3306`

To switch from SQLite to MySQL, update `SQLALCHEMY_DATABASE_URI` in `src/config/data_base.py` as indicated in comments.

## Running the Project

### Option 1: Local (without Docker)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables (`.env` or shell exports).
4. Run:

```bash
flask --app run.py run
```

API will be available at `http://localhost:5000`.

### Option 2: Docker Compose

1. Ensure `.env` exists with Twilio variables.
2. Run:

```bash
docker compose up --build
```

Containers:

- `web`: Flask API on `http://localhost:5000`
- `mysql57`: MySQL on `127.0.0.1:3306`

## API Endpoints

Base URL: `http://localhost:5000`

### `GET /`

Health check.

Example response:

```json
{
  "message": "Server is running"
}
```

### `GET /api`

API status endpoint.

Example response:

```json
{
  "mensagem": "API - OK; Docker - Up"
}
```

### `POST /user`

Creates a user/seller and triggers Twilio WhatsApp activation send.

Request body:

```json
{
  "nome": "Mini Mercado X",
  "cnpj": "12345678000199",
  "email": "mercado@email.com",
  "celular": "5511999999999",
  "senha": "123456"
}
```

Success response (`200`):

```json
{
  "mensagem": "Usuario salvo com sucesso. Verifique o WhatsApp.",
  "usuarios cadastrados": {},
  "whatsapp": {
    "sid": "SMxxxxxxxx",
    "status": "queued",
    "to": "whatsapp:+5511999999999"
  }
}
```

Possible errors:

- `400`: required field missing
- `401`: invalid CNPJ or phone length
- `502`: user created but WhatsApp sending failed

### `GET /testarNumero`

Sends a Twilio WhatsApp message to a fixed number for integration testing.

Success response (`200`):

```json
{
  "sid": "SMxxxxxxxx",
  "status": "queued",
  "to": "whatsapp:+5511958942521"
}
```

Error response (`500`):

```json
{
  "erro": "..."
}
```

## Useful cURL Commands

Create user:

```bash
curl -X POST http://localhost:5000/user \
  -H "Content-Type: application/json" \
  -d "{\"nome\":\"Mini Mercado X\",\"cnpj\":\"12345678000199\",\"email\":\"mercado@email.com\",\"celular\":\"5511999999999\",\"senha\":\"123456\"}"
```

API health:

```bash
curl http://localhost:5000/api
```

Twilio test:

```bash
curl http://localhost:5000/testarNumero
```

## Troubleshooting

- `KeyError: TWILIO_ACCOUNT_SID`:
  - Ensure `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` are set.
- Twilio send failures:
  - Validate credentials, sandbox number format, and allowed destination in Twilio.
- Database issues:
  - Confirm selected database URI in `src/config/data_base.py`.
  - For MySQL, verify `mysql57` container is running.

## Security Notes

- Rotate any Twilio credentials that were exposed in commits or screenshots.
- Do not store production secrets in repository files.
