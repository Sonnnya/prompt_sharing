from typing import Annotated
from fastapi import APIRouter, Depends
from models.prompts import PromptPydantic, PromptInPydantic
from services.prompts import list_all_prompts, get_single_prompt, add_prompt, PromptException, rate_prompt
from starlette.responses import Response
from fastapi_pagination.iterables import LimitOffsetPage
from typing import Optional, Literal
from fastapi import Query
router = APIRouter()


@router.get('/')
async def list_prompts(category_id: Optional[int] = Query(
        None,
    description="ID категории для фильтрации",
    ),
    search: Optional[str] = Query(None,
                                  description="Поиск по названию или описанию"),
    sort_by_rating: Literal['desc', ''] = Query(None,
                                                description="Сортировка по рейтингу ('asc' или 'desc')")) -> LimitOffsetPage[PromptPydantic]:
    result = await list_all_prompts(category_id, search, sort_by_rating)
    return result


@router.get('/{prompt_id}', responses={404: {'description': 'prompt not found'}})
async def get_prompt_by_id(prompt_id: int) -> PromptPydantic:
    try:
        prompt = await get_single_prompt(prompt_id)
    except PromptException as e:
        return Response('There is no such prompt', status_code=404)
    return prompt


@router.post('/', response_model=PromptPydantic)
async def create_prompt(prompt: PromptInPydantic) -> PromptPydantic:
    return await add_prompt(prompt)


@router.post('/{prompt_id}/rate')
async def rate(prompt_id: int) -> PromptPydantic:
    try:
        prompt = await rate_prompt(prompt_id)
    except PromptException:
        return Response('There is no such prompt', status_code=404)
    return prompt
