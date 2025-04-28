from typing import Annotated
from fastapi import APIRouter
from models.categories import CatPydantic, CatInPydantic
from services.categories import list_all_cats
from starlette.responses import Response
from services.categories import add_cat

router = APIRouter()


@router.get('/')
async def list_cats() -> dict[str, list[CatPydantic]]:
    result = await list_all_cats()
    return {"items": result}


@router.post('/')
async def add_category(cat: CatInPydantic) -> CatPydantic:
    return await add_cat(cat)
