from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_core.runnables import Runnable
from pydantic_core import Url


class ImageOutputParser:
    def __init__(self, chain: Runnable, content: str) -> None:
        self._chain = chain
        self._content = content
        self._model = DallEAPIWrapper(
            model='dall-e-3',
            quality='standard',
            size='1024x1024',
        )  # type: ignore

    def draw(self, input: str, output: str) -> Url:
        query = self._chain.invoke({
            'input_context': input,
            'chat_suffix': [
                SystemMessage(
                    content=output,
                ),
                HumanMessage(
                    content=self._content,
                ),
            ],
        })
        print(query)

        return Url(self._model.run(query))


def build(name: str, chain: Runnable) -> ImageOutputParser:
    # Load the prompt content
    with open(f'./prompts/{name}_image.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    return ImageOutputParser(
        chain=chain,
        content=content,
    )
