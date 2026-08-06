from sqlalchemy import String, Integer #, Numeric(소숫점 포함)
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class BookModel(Base):
    __tablename__ = "books"

    id : Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    isbn: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )