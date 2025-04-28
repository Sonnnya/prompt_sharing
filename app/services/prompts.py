from models.prompts import PromptPydantic, PromptInPydantic
from db.models.prompt import Prompt
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import F, Q
from fastapi_pagination.ext.tortoise import paginate
from typing import Optional, Literal
from fastapi_pagination.iterables import LimitOffsetPage


class PromptException(BaseException):
    pass


async def list_all_prompts(
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        sort_by_rating: Literal['desc', ''] = '',
) -> LimitOffsetPage[PromptPydantic]:  # type: ignore
    query = Prompt.all().prefetch_related('categories')

    if category_id:
        query = query.filter(categories__id=category_id)

    if search:
        query = query.filter(Q(title__icontains=search) |
                             Q(description__icontains=search))

    if sort_by_rating:
        query = query.order_by(
            f'{'-' if sort_by_rating == 'desc' else ''}rating')

    return await paginate(query)


async def get_single_prompt(prompt_id: int) -> PromptPydantic:  # type: ignore
    try:
        prompt = await PromptPydantic.from_queryset_single(
            Prompt.get(id=prompt_id).prefetch_related('categories')
        )
    except DoesNotExist:
        raise PromptException("Prompt not found")
    return prompt


async def add_prompt(prompt: PromptInPydantic) -> PromptPydantic:
    prompt_obj = await Prompt.create(
        **prompt.model_dump(exclude_unset=True)
    )
    return await PromptPydantic.from_tortoise_orm(prompt_obj)


async def rate_prompt(prompt_id: int) -> PromptPydantic:
    # одним запросом, можно select_for_update, чтобы не было проблем с
    # большим кол-вом записей в один момент
    await Prompt.filter(id=prompt_id).update(rating=F('rating') + 1)
    prompt = await Prompt.get(id=prompt_id)
    return await PromptPydantic.from_tortoise_orm(prompt)
