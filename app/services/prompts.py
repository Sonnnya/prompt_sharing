from models.prompts import PromptPydantic, PromptInPydantic
from db.models.prompt import Prompt
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import F
from fastapi_pagination.ext.tortoise import paginate


class PromptException(BaseException):
    pass


async def list_all_prompts() -> list[PromptPydantic]:  # type: ignore
    return await paginate(
        Prompt.all().prefetch_related('categories')
    )


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
