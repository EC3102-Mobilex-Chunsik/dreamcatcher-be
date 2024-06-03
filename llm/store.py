from langchain_core.language_models.llms import LLM

from models.base.llm import (
    BaseLLMModel,
    ChatGPTModel,
    HuggingFaceEndpointModel,
)

_MODELS: list[BaseLLMModel] = [
    ChatGPTModel(
        name='chatgpt',
    ),
    HuggingFaceEndpointModel(
        name='huggingface',
    ),
]


def _find_model(name: str) -> BaseLLMModel | None:
    return next(
        (
            model
            for model in _MODELS
            if model.name == name
        ),
        None
    )


class LLMStore:
    def __init__(self) -> None:
        self._children: dict[BaseLLMModel, LLM] = {}

    def _load(self, model: BaseLLMModel) -> LLM:
        if model not in self._children:
            self._children[model] = model.build()
        return self._children[model]

    def get(
        self,
        model_name: str | None = None,
    ) -> LLM:
        if model_name is not None:
            model = _find_model(model_name)
            if model is None:
                raise ValueError(f'No such LLM model: {model_name!r}')
        else:
            model = next(iter(_MODELS), None)
            if model is None:
                raise ValueError('LLM Model is not set')

        return self._load(model)
