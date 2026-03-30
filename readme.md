# Money Flow

A REST API for personal expense tracking with multi-account support and atomic transactions.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-built--in-lightgrey?style=flat-square)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)

---

## Features

- Create accounts with balances (cash, card, etc.)
- Record expenses linked to an account
- Transfer money between accounts
- Top up account balance
- Filter expenses by category
- Calculate total spending (overall or by category)
- Edit or delete expenses with automatic balance correction
- Atomic transactions — balance and expense update together or not at all

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Database | SQLite (stdlib `sqlite3`) |
| Config | `python-dotenv` |
| Testing | pytest, `tmp_path`, `monkeypatch` |

---

## Project Structure

```
money_flow/
├── api/
│   ├── routes_accounts.py  # account endpoints
│   └── routes_expenses.py  # expense endpoints
├── tests/
│   ├── conftest.py
│   ├── test_account.py
│   └── test_expenses.py
├── models.py               # Expense, Account dataclasses
├── schemas.py              # Pydantic request/response models
├── services.py             # business logic
├── repositories.py         # SQL queries
├── database.py             # connection management
├── dependencies.py         # FastAPI DI
├── exceptions.py           # custom exceptions
├── exception_handlers.py   # error responses
├── config.py               # env-based config
└── main.py                 # app entry point
```

---

## Installation

```bash
git clone https://github.com/Zhelero/money_flow
cd money_flow

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DB_NAME=expenses.db
LOG_LEVEL=INFO
DEBUG=false
```

Run:

```bash
uvicorn money_flow.main:app --reload
```

API docs: `http://localhost:8000/docs`

---

## API Overview

### Accounts

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/accounts/` | Create account |
| `GET` | `/accounts/` | List all accounts |
| `POST` | `/accounts/{name}/topup` | Top up balance |
| `POST` | `/accounts/transfer` | Transfer between accounts |

### Expenses

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/expenses/` | Record expense |
| `GET` | `/expenses/` | List expenses (optional `?category=`) |
| `PATCH` | `/expenses/{id}` | Edit expense |
| `DELETE` | `/expenses/{id}` | Delete expense |
| `GET` | `/expenses/total` | Total spent (optional `?category=`) |

---

## API Examples

### Create account

```bash
curl -X POST http://localhost:8000/accounts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Cash", "balance": 500}'
```

```json
{"name": "Cash", "balance": 500}
```

### Record expense

```bash
curl -X POST http://localhost:8000/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 45.50, "money_source": "Cash", "category": "Food"}'
```

```json
{
  "deal_id": 1,
  "amount": 45.5,
  "money_source": "Cash",
  "category": "Food",
  "created_at": "2026-03-30T14:00:00"
}
```

### Transfer between accounts

```bash
curl -X POST http://localhost:8000/accounts/transfer \
  -H "Content-Type: application/json" \
  -d '{"from_account": "Cash", "to_account": "Card", "amount": 100}'
```

### Get total by category

```bash
curl http://localhost:8000/expenses/total?category=Food
```

```json
{"total": 145.5}
```

---

## Testing

```bash
pytest
```

Tests use `tmp_path` + `monkeypatch` — each test gets a fresh isolated database,
no cleanup needed.

Key scenarios covered:

- Expense creation deducts balance atomically
- Editing an expense recalculates the balance difference
- Changing `money_source` on an expense moves the charge to the new account
- Deleting an expense restores the balance
- Transfer rolls back if source account has insufficient funds
- Duplicate account creation returns 400
- All `NotFound` cases return 404

---

## Key Design Decisions

**Atomic transactions** — spending, editing, and deleting expenses update both
the `expenses` table and the account balance in a single SQL transaction.
If anything fails, both changes are rolled back together.

**Edit recalculates balance** — editing an expense amount doesn't just update
the record. It computes the difference and adjusts the account balance accordingly.
Same logic applies when changing `money_source` — the old account is refunded and
the new one is charged.

**Custom exception hierarchy** — all domain errors inherit from `MoneyFlowError`
with a `status_code` field, keeping HTTP error handling out of the business logic.
