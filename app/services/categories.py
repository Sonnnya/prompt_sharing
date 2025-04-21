from models.categories import CatPydantic
from db.models.category import Category
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import F


class CatException(BaseException):
    pass


async def list_all_cats() -> list[CatPydantic]:  # type: ignore
    return await CatPydantic.from_queryset(
        Category.all()
    )
