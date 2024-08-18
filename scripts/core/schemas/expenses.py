from pydantic import BaseModel, Field
from typing import Optional
import shortuuid

class CreateExpense(BaseModel):
    user_id: Optional[str] = Field(title="Category created by user", default="")
    amount: int = Field(title="Amount spent")
    note: str = Field(title="Note for the expense")
    transaction_date: str = Field(title="Transaction date time")
    category_id: str = Field(title="Category Id of expense")
    expense_id: str = Field(default=shortuuid.ShortUUID().random(length=6))
    expense_name: str = Field(title="Expense Name")



