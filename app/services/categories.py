from models.categories import CatPydantic, CatInPydantic
from db.models.category import Category
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import F
from db.models.category import Category


class CatException(BaseException):
    pass


async def list_all_cats() -> list[CatPydantic]:  # type: ignore
    return await CatPydantic.from_queryset(
        Category.all()
    )


async def add_cat(category: CatInPydantic) -> CatPydantic:
    cat_obj = await Category.create(**category.model_dump())
    return await CatPydantic.from_tortoise_orm(cat_obj)
