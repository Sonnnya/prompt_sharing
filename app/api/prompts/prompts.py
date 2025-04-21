from typing import Annotated
from fastapi import APIRouter, Depends
from models.prompts import PromptPydantic, PromptInPydantic
from services.prompts import list_all_prompts, get_single_prompt, add_prompt, PromptException, rate_prompt
from starlette.responses import Response

router = APIRouter()


@router.get('/')
async def list_prompts() -> dict[str, list[PromptPydantic]]:
    result = await list_all_prompts()
    return {"items": result}


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
