import datetime

from scripts.utils.session_util import Base
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column


class UserDetailsOrmSchema(Base):
    __tablename__ = "user_details"
    email: Mapped[str] = mapped_column(index=True)
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(default="")
    password: Mapped[str] = mapped_column(index=True)
    user_id: Mapped[str] = mapped_column(index=True, primary_key=True)


class CategoriesOrmSchema(Base):
    __tablename__ = "category"
    user_id: Mapped[str] = mapped_column(ForeignKey("user_details.user_id"))
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    category_id: Mapped[str] = mapped_column(index=True, primary_key=True)

    idx_all = Index(
        "idx_category_all",
        user_id,
        title,
        description,
        category_id,
        postgresql_using="btree",
    )


class TransactionOrmSchema(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    category_id: Mapped[str] = mapped_column(
        ForeignKey("category.category_id"), index=True
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("user_details.user_id"), index=True)
    amount: Mapped[int] = mapped_column(index=True)
    note: Mapped[str] = mapped_column(index=True)
    transaction_date: Mapped[datetime.datetime] = mapped_column(index=True)
    expense_id: Mapped[str] = mapped_column(index=True)
    expense_name: Mapped[str] = mapped_column(index=True)
    idx_all = Index(
        "idx_transaction_all",
        user_id,
        category_id,
        transaction_date,
        amount,
        postgresql_using="btree",
    )
    idx_transaction_date_btree = Index(
        "idx_transaction_date_btree",
        transaction_date,
        postgresql_using="btree",
    )
    idx_transaction_date_hash = Index(
        "idx_transaction_date_hash",
        transaction_date,
        postgresql_using="hash",
    )
