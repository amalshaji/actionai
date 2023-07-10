from typing import Any, Dict, List, Literal, Optional, TypedDict


class _MessageBase(TypedDict):
    role: str
    content: str


class Message(_MessageBase, total=False):
    name: Optional[str]


class _BaseChatResponseMessage(TypedDict):
    role: str
    content: Optional[str]


class ChatResponseFunctionCall(TypedDict):
    name: str
    arguments: str


class ChatResponseMessage(_BaseChatResponseMessage):
    function_call: ChatResponseFunctionCall


class ChatResponseChoices(TypedDict):
    index: int
    message: ChatResponseMessage
    finish_reason: str


class ChatResponseUsage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(TypedDict):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatResponseChoices]
    usage: ChatResponseUsage


class OpenAIFunction(TypedDict):
    name: str
    description: str
    parameters: Dict[str, Any]


OPENAI_MODELS = Literal[
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
]
