from langchain_core.language_models.llms import LLM
from langchain_core.messages.system import SystemMessage
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


def build(name: str, llm: LLM):
    # Load the prompt content
    with open(f'./prompts/{name}.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(
                variable_name='chat_prefix',
                optional=True,
            ),
            SystemMessage(content=content),
            MessagesPlaceholder(
                variable_name='chat_history',
                optional=True,
            ),
            HumanMessagePromptTemplate.from_template('{input_context}'),
            MessagesPlaceholder(
                variable_name='chat_suffix',
                optional=True,
            ),
        ]
    )

    # Attach an output parser
    output_parser = StrOutputParser()

    # Create a LLM chain with given content
    return prompt | llm | output_parser
