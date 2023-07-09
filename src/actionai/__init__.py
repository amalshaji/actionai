import json
from typing import Any, Callable, cast

import openai
from attr import dataclass

from actionai.exceptions import ActionAIException
from actionai.json_schema import create_json_schema_for_function_input
from actionai.types import (
    OPENAI_MODELS,
    ChatResponse,
    ChatResponseMessage,
    Message,
    OpenAIFunction,
)


@dataclass
class ActionAIFunction:
    fn: Callable
    name: str
    description: str
    input_schema: Any


class ActionAI:
    def __init__(
        self,
        openai_api_key: str | None = None,
        context: dict[str, Any] | None = None,
        model: OPENAI_MODELS = "gpt-3.5-turbo-0613",
    ) -> None:
        """
        Args:
            openai_api_key (str | None, optional): If not set, defaults \
                to `OPENAI_API_KEY` environment variable.

            context (dict[str, Any] | None, optional): These keys will be skipped \
                when creating json schema for the function's input. The values \
                    will be directly passed during function call.

            model (optional): The chat completion model to use. Defaults to \
                "gpt-3.5-turbo-0613".
        """
        if openai_api_key is not None:
            openai.api_key = openai_api_key

        self.functions: dict[str, ActionAIFunction] = {}
        self.messages: list[Message | ChatResponseMessage] = []
        self.openai_functions: list[OpenAIFunction] = []
        self.context = context or {}
        self.model = model

    def register(self, fn: Callable):
        if fn.__name__ in self.functions:
            raise ActionAIException("function with the same name already registered")

        if fn.__doc__ is None:
            raise ActionAIException("function must have a docstring")

        action_function = ActionAIFunction(  # type: ignore #TODO: Fix this
            fn=fn,
            name=fn.__name__,
            description=fn.__doc__,
            input_schema=create_json_schema_for_function_input(
                fn=fn, skip_keys=list(self.context.keys())
            ),
        )
        self.functions[fn.__name__] = action_function
        self.openai_functions.append(
            {
                "name": action_function.name,
                "description": action_function.description,
                "parameters": action_function.input_schema,
            }
        )

    def prompt(self, query: str) -> ChatResponse:
        self.messages.append({"role": "user", "content": query})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            functions=self.openai_functions,
            function_call="auto",
        )

        response = cast(ChatResponse, response)

        response_message = response["choices"][0]["message"]

        if response_message.get("function_call") is None:
            return response

        function_name = response_message["function_call"]["name"]
        fuction_to_call = self.functions[function_name].fn
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(**function_args, **self.context)

        self.messages.append(response_message)
        self.messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response, default=str),
            }
        )
        second_response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
        )
        second_response = cast(ChatResponse, second_response)
        return second_response
