# Wallet Service

A JSON:API compliant service for managing wallets and transactions.

## Requirements

- Docker and Docker Compose
- PostgreSQL 14+
- Python 3.11+

## API Endpoints

### Wallets
- `GET /api/wallets/` - list all wallets
- `POST /api/wallets/` - create a wallet
- `GET /api/wallets/{id}/` - get wallet details
- `PATCH /api/wallets/{id}/` - update wallet
- `DELETE /api/wallets/{id}/` - delete wallet

### Transactions
- `GET /api/transactions/` - list transactions
- `POST /api/transactions/` - create a transaction
- `GET /api/transactions/{id}/` - get transaction details

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/B2BinPay-Oleinik/test_project/
cd wallet-service
```

2. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` with your settings:
- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Change to a secure random string
- `ALLOWED_HOSTS`: Add your domain names
- `POSTGRES_DB`: Your PostgreSQL database name
- `POSTGRES_USER`: PostgreSQL database user name
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `POSTGRES_PORT`: PostgreSQL service port

3. Start the service:
```bash
docker-compose up
```

The API will be available at http://localhost:8000/api/

## Examples

### Pagination

```bash
# Second page of wallets list using a default page size
GET /api/wallets?page[number]=2

# First page of transactions list using a custom page size
GET /api/transactions?page[size]=10
```

### Sorting

```bash
# Sort transactions by amount (descending)
GET /api/transactions?sort=-amount

# Sort wallets by balance (ascending)
GET /api/wallets?sort=balance
```

### Filtering

```bash
# Get wallets with balance >= 100
GET /api/wallets?filter[balance.gte]=100

# Search wallets by label (case-insensitive)
GET /api/wallets?filter[label.icontains]=test_wallet

# Get transactions for specific wallet
GET /api/transactions?filter[wallet]=1
```

## Development Setup

### Running the project locally

1. Set up Git hooks:
```bash
git config core.hooksPath hooks
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` with your settings:
- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Change to a secure random string
- `ALLOWED_HOSTS`: Add your domain names
- `POSTGRES_DB`: Your PostgreSQL database name
- `POSTGRES_USER`: PostgreSQL database user name
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `POSTGRES_PORT`: PostgreSQL service port

5. Set up PostgreSQL and create database:
```bash
source .env && createdb "${POSTGRES_DB}"
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

### Code quality tools

#### Ruff

```bash
# Run Ruff with auto-fix using unsafe fixes
ruff check . --fix --unsafe-fixes
```

#### Pytest

```bash
# Run tests with coverage report in HTML format
pytest --cov=wallets --cov-report=html
```
