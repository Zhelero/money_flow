# Money Flow

A simple transactional money management system built with Python and SQLite.

## 📌 Features

- Create accounts
- Transfer money between accounts
- Spend money with category tracking
- Edit expenses (with atomic balance correction)
- Delete expenses (with automatic refund)
- View total expenses (optionally filtered by category)
- Full transaction safety with rollback
- Unit tested with pytest

---

## 🏗 Architecture

The project follows a layered architecture:

Service → Repository → SQLite

- **Services** contain business logic.
- **Repositories** handle database operations.
- **Database** initializes schema.
- **Models** represent domain objects.
- **Exceptions** define domain-specific errors.

All critical operations (transfer, spend, edit, delete) are atomic.

---

## 🗂 Project Structure
money_flow/
database.py
repositories.py
services.py
models.py
exceptions.py
config.py
main.py

tests/
test_account.py
test_expenses.py


---

## 🚀 Installation

Clone the repository:

```bash
git clone <repo_url>
cd Money_flow

Create virtual environment:

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
▶ Running the Application

Run as a module:

python -m money_flow.main
🧪 Running Tests
python -m pytest

With coverage:

python -m pytest --cov=money_flow --cov-report=term-missing

🔒 Data Integrity
The system guarantees:
No negative balances
No duplicate accounts
Atomic transfers
Automatic rollback on failure
Expense deletion refunds money


📚 Technologies
Python 3.13
SQLite
pytest
pytest-cov