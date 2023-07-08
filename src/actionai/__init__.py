import json
from typing import Any, Callable, cast

import openai
from attr import dataclass

from actionai.json_schema import create_json_schema_for_function_input
from actionai.types import ChatResponse, ChatResponseMessage, Message


class ActionAIException(Exception):
    pass


@dataclass
class ActionAIFunction:
    fn: Callable
    name: str
    description: str
    input_schema: Any


class ActionAI:
    def __init__(self, openai_api_key: str | None = None) -> None:
        if openai_api_key is not None:
            openai.api_key = openai_api_key

        self.functions: dict[str, ActionAIFunction] = {}
        self.messages: list[Message | ChatResponseMessage] = []
        self.openai_functions: list | None = None

    def register(self, fn: Callable):
        if fn.__name__ in self.functions:
            raise ActionAIException(
                "function with the same name already registered"
            )

        if fn.__doc__ is None:
            raise ActionAIException("function must have a docstring")

        self.functions[fn.__name__] = ActionAIFunction(  # type: ignore #TODO: Fix this
            fn=fn,
            name=fn.__name__,
            description=fn.__doc__,
            input_schema=create_json_schema_for_function_input(fn),
        )

    def _set_openai_functions(self):
        if self.openai_functions is not None:
            return

        self.openai_functions = []
        for fun in self.functions.values():
            self.openai_functions.append(
                {
                    "name": fun.name,
                    "description": fun.description,
                    "parameters": fun.input_schema,
                }
            )

    def prompt(self, query: str) -> ChatResponse:
        self._set_openai_functions()
        self.messages.append({"role": "user", "content": query})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
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
        function_args = json.loads(
            response_message["function_call"]["arguments"]
        )
        function_response = fuction_to_call(**function_args)

        self.messages.append(response_message)
        self.messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response, default=str),
            }
        )
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=self.messages,
        )
        second_response = cast(ChatResponse, second_response)
        return second_response
