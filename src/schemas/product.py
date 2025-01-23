from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    PositiveInt,
    field_validator,
)


class ProductSchemaBase(BaseModel):
    """Base schema for product."""

    name: str = Field(
        min_length=1,
        max_length=250,
        title="Name product.",
        description=(
            "Уникальное название товара, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 250 символов включительно;"
        ),
    )
    article: PositiveInt = Field(
        title="Articul product from store.",
        description=(
            "Артикул товара в магазине, целочисленное уникальное значение."
        ),
    )
    price: PositiveFloat = Field(
        title="Price product.",
        description=(
            "Цена товара, рубли, положительное число с плавающей запятой."
        ),
    )
    rating: float = Field(
        title="Rating product from store.",
        description=(
            "Рейтинг товара на основе отзывов, число с "
            "плавающей запятой от 0 до 5 включительно."
        ),
    )
    total: int = Field(
        title="Total product from warehouse.",
        description="Количесво товара на всех складах.",
    )
    perform_update: Optional[bool] = Field(
        None,
        title="Perform update and over time.",
        description="Обновлять ли товар при запуске, или по времени.",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Бомбочки для ванны набор",
                "article": 122551613,
                "price": 387.00,
                "rating": 4.7,
                "total": 10560,
            }
        }

    @field_validator("rating")
    def rating_validator(cls: "ProductSchemaBase", value: int) -> int:
        if value < 0 and value > 5:
            except_message = (
                f"Значение {value} должно быть в "
                "диапазоне от 0 до 5-ти включительно."
            )
            return ValueError(except_message)
        return value

    def __repr__(self) -> str:
        return f"Товар: Артикул {self.article} Количество {self.total}"


class ProductSchemaCreate(ProductSchemaBase):
    """Schema for create product."""


class ProductSchemaUpdate(ProductSchemaBase):
    """Schema for update product."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        title="Name product.",
        description=(
            "Уникальное название товара, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 250 символов включительно;"
        ),
    )
    article: Optional[PositiveInt] = Field(
        None,
        title="Articul product from store.",
        description=(
            "Артикул товара в магазине, целочисленное уникальное значение."
        ),
    )
    price: Optional[PositiveFloat] = Field(
        None,
        title="Price product.",
        description=(
            "Цена товара, рубли, положительное число с плавающей запятой."
        ),
    )
    rating: Optional[float] = Field(
        None,
        title="Rating product from store.",
        description=(
            "Рейтинг товара на основе отзывов, число с "
            "плавающей запятой от 0 до 5 включительно."
        ),
    )
    total: Optional[int] = Field(
        None,
        title="Total product from warehouse.",
        description="Количесво товара на всех складах.",
    )

    class Config:
        extra = "forbid"


class ProductSchemaDB(ProductSchemaBase):
    """Presentate schema for product in database."""

    id: int = Field(
        title="Id product in db", description="Id товара в базе данных"
    )
    perform_update: Optional[bool] = Field(
        None,
        title="Perform update and over time.",
        description="Обновлять ли товар при запуске, или по времени.",
        exclude=True,
    )

    class Config:
        from_attributes: bool = True


class ProductSchemaGetFromStore(BaseModel):
    """Schema for get product from store."""

    article: PositiveInt = Field(
        title="Articul product from store.",
        description=(
            "Артикул товара в магазине, целочисленное уникальное значение."
        ),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "article": 122551613,
            }
        }
