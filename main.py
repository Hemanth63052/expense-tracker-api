import gc

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.config import API_CONF
from scripts.core.services.categories.category_services import category_router
from scripts.core.services.expenses.expense_service import expense_router
from scripts.core.services.user_auth.user_services import user_router
from scripts.utils.cookie_auth import CookieAuthentication

gc.collect()

auth = CookieAuthentication()
app = FastAPI(
    title="Expense Tracker",
    version="0.0.1",
    description="Expense Tracker include User Authentication ",
    openapi_url=API_CONF.SW_OPENAPI_URL,
    docs_url=API_CONF.SW_DOCS_URL,
    redoc_url=API_CONF.RE_DOCS_URL,
    root_path="/api",
)
auth_enabled = (
    [Depends(auth)] if API_CONF.SECURE_ACCESS in [True, "true", "True"] else None
)

app.include_router(user_router)
app.include_router(category_router, dependencies=auth_enabled)
app.include_router(expense_router, dependencies=auth_enabled)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)
