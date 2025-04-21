from typing import Annotated
from fastapi import APIRouter
from models.categories import CatPydantic
from services.categories import list_all_cats
from starlette.responses import Response

router = APIRouter()


@router.get('/')
async def list_cats() -> dict[str, list[CatPydantic]]:
    result = await list_all_cats()
    return {"items": result}
