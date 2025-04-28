from tortoise.contrib.pydantic import pydantic_model_creator

from db.models.category import Category

CatPydantic = pydantic_model_creator(
    Category,
    exclude=('updated_at'),
)

CatInPydantic = pydantic_model_creator(
    Category,
    exclude=('updated_at'),
    exclude_readonly=True
)
