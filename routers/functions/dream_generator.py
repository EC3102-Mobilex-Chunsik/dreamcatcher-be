import os
from fastapi import APIRouter
from llm.chat import build
from llm.store import LLMStore
from models.dream_generator import InputModel, OutputModel, DreamDetailModel
from typing import List

# Configure API router
router = APIRouter(
    tags=['dreams'],
)

# Configure metadata
NAME = os.path.basename(__file__)[:-3]

# Configure resources
store = LLMStore()

###############################################
#                   Actions                   #
###############################################

# Dream List


@router.get('/dreams', response_model=List[DreamDetailModel])
async def get_all_dreams() -> List[DreamDetailModel]:
    # Retrieve all dream records from the database
    dreams = store.get_all_dreams()
    return dreams

# Dream Detail by ID


@router.get('/dreams/{id}', response_model=DreamDetailModel)
async def get_dream_by_id(id: int) -> DreamDetailModel:
    # Retrieve specific dream by ID from the database
    dream = store.get_dream_by_id(id)
    return dream

# Dream Generation


@router.post(f'/func/{NAME}', response_model=OutputModel)
async def call_dream_generator(model: InputModel) -> OutputModel:
    # Create a LLM chain
    chain = build(
        name=NAME,
        llm=store.get(model.llm_type),
    )

    generated_dream = chain.invoke({
        'input_context': model.text,
    })

    return OutputModel(
        title=generated_dream['title'],
        context=generated_dream['context'],
        factors=generated_dream['factors'],
        images=generated_dream['images'],
    )
