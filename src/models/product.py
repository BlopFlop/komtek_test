from sqlalchemy import BigInteger, Boolean, CheckConstraint, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Product(Base):
    """Product model."""

    name: Mapped[str] = mapped_column(
        String(250),
        CheckConstraint("LENGTH(name) <= 250", name="check_len_name"),
        unique=True,
        nullable=False,
        comment=(
            "Уникальное название товара, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 250 символов включительно;"
        ),
    )
    article: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        comment="Артикул товара в магазине, целочисленное уникальное значение.",
    )
    price: Mapped[float] = mapped_column(
        Float,
        CheckConstraint("price > 0", name="check_price_positive"),
        unique=False,
        nullable=False,
        comment="Цена товара, положительное число с плавающей запятой.",
    )
    rating: Mapped[Float] = mapped_column(
        Float,
        CheckConstraint("0 <= rating <= 5", name="check_rating"),
        unique=False,
        nullable=False,
        comment=(
            "Рейтинг товара, число с плавающей запятой от 0 до 5 включительно."
        ),
    )
    total: Mapped[int] = mapped_column(
        BigInteger,
        unique=False,
        nullable=False,
        comment="Количесво товара на всех складах.",
    )
    perform_update: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=True,
        comment="Обновлять ли товар при запуске, или по времени.",
    )

    def __repr__(self) -> str:
        return f"Product: Articul {self.article} Total {self.total}"
