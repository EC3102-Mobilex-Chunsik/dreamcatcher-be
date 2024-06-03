from typing import Literal, List
from pydantic import BaseModel, Field
import openai

# OpenAI API 키 설정 (환경 변수로 설정하는 것이 더 안전합니다)
openai.api_key = 'api_key'


class FactorModel(BaseModel):
    tagName: str
    description: str


class InputModel(BaseModel):
    dream_description: str = Field(
        description='사용자가 묘사하는 꿈의 내용',
        default='어젯밤에 나는 하늘을 나는 꿈을 꾸었어',
    )

    llm_type: Literal['chatgpt', 'huggingface'] = Field(
        alias='Large Language Model Type',
        description='사용할 LLM 종류',
        default='chatgpt',
    )


class OutputModel(BaseModel):
    interpretation: str = Field(
        description='꿈 해석',
    )


def interpret_dream(input_data: InputModel) -> OutputModel:
    # dream.txt 파일의 내용을 읽어옵니다.
    with open('../prompts/dream.txt', 'r', encoding='utf-8') as file:
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


def main():
    # 예제 사용자 입력
    user_input = {
        "dream_description": "어젯밤에 나는 하늘을 나는 꿈을 꾸었어",
        "llm_type": "chatgpt"
    }

    input_data = InputModel(**user_input)
    output_data = interpret_dream(input_data)

    print("꿈 해석 결과:", output_data.interpretation)


if __name__ == "__main__":
    main()
