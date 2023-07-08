from typing import Any, TypedDict


class _MessageBase(TypedDict):
    role: str
    content: str


class Message(_MessageBase, total=False):
    name: str | None


class _BaseChatResponseMessage(TypedDict):
    role: str
    content: str | None


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
    choices: list[ChatResponseChoices]
    usage: ChatResponseUsage


class OpenAIFunction(TypedDict):
    name: str
    description: str
    parameters: dict[str, Any]
