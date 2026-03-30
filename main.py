#Money Flow 2.0. API
from fastapi import FastAPI
from exception_handlers import register_exception_handlers
from api.routes_accounts import router as accounts_router
from api.routes_expenses import router as expenses_router

app = FastAPI(title="Money Flow API")

register_exception_handlers(app)

app.include_router(accounts_router)
app.include_router(expenses_router)