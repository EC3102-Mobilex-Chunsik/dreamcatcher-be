from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
import openai
import os
import logging

# Configure API router
router = APIRouter(
    tags=['dreams'],
)

# 설정 로그
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API 키 설정 (환경 변수에서 읽어오기)
openai.api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
if not openai.api_key:
    logger.error("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
else:
    logger.info(f"OPENAI_API_KEY 설정됨: {openai.api_key}")


class InputModel(BaseModel):
    dream_description: str = Field(
        description='사용자가 묘사하는 꿈의 내용',
        default='어젯밤에 나는 하늘을 나는 꿈을 꾸었어..',
    )
    llm_type: Literal['chatgpt', 'huggingface'] = Field(
        description='사용할 LLM 종류',
        default='chatgpt',
    )


class OutputModel(BaseModel):
    interpretation: str = Field(
        description='꿈 해석',
    )


def interpret_dream(input_data: InputModel) -> OutputModel:
    # dream.txt 파일의 내용을 읽어옵니다.
    with open('./prompts/dream.txt', 'r', encoding='utf-8') as file:
        dream_prompt = file.read()

    if input_data.llm_type == 'chatgpt':
        # OpenAI API를 사용하여 GPT-4 모델 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5",
            messages=[
                {"role": "system", "content": "You are a dream interpreter."},
                {"role": "system", "content": dream_prompt},
                {"role": "user", "content": f"다음 꿈을 해석해줘: {input_data.dream_description}"}
            ]
        )
        interpretation = response['choices'][0]['message']['content'].strip()
    else:
        raise ValueError(f"지원하지 않는 LLM 타입: {input_data.llm_type}")

    return OutputModel(interpretation=interpretation)


# 새로운 꿈 해석 엔드포인트
@router.post("/interpret", response_model=OutputModel)
def interpret_dream_endpoint(input_data: InputModel):
    return interpret_dream(input_data)
