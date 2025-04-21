from api.prompts.prompts import router as prompts_router
from api.categories.categories import router as cat_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(prompts_router, prefix="/api/prompts", tags=["prompts"])
router.include_router(
    cat_router, prefix="/api/categories", tags=["categories"])

__all__ = ["router"]
