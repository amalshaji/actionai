import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union, cast

import openai

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

    def to_openai_function(self) -> OpenAIFunction:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.input_schema,
        }


class ActionAI:
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        model: OPENAI_MODELS = "gpt-3.5-turbo-0613",
    ) -> None:
        """
        Args:
            openai_api_key (Optional[str]): If not set, defaults \
                to `OPENAI_API_KEY` environment variable.

            context (Optional[Dict[str, Any]]): These keys will be skipped \
                when creating json schema for the function's input. The values \
                    will be directly passed during function call.

            model (optional): The chat completion model to use. Defaults to \
                "gpt-3.5-turbo-0613".
        """
        if openai_api_key is not None:
            openai.api_key = openai_api_key

        self.messages: List[Union[Message, ChatResponseMessage]] = []
        self.context = context or {}
        self.model = model

        # Do not update these attributes directly
        self._functions: Dict[str, ActionAIFunction] = {}
        self._openai_functions: List[OpenAIFunction] = []

    def register(self, fn: Callable):
        if fn.__name__ in self._functions:
            raise ActionAIException("function with the same name already registered")

        if fn.__doc__ is None:
            raise ActionAIException("function must have a docstring")

        action_function = ActionAIFunction(
            fn=fn,
            name=fn.__name__,
            description=fn.__doc__,
            input_schema=create_json_schema_for_function_input(
                fn=fn, skip_keys=list(self.context.keys())
            ),
        )
        self._functions[fn.__name__] = action_function
        self._openai_functions.append(action_function.to_openai_function())

    def prompt(self, query: str) -> ChatResponse:
        self.messages.append({"role": "user", "content": query})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            functions=self._openai_functions,
            function_call="auto",
        )

        response = cast(ChatResponse, response)

        response_message = response["choices"][0]["message"]

        if response_message.get("function_call") is None:
            return response

        function_name = response_message["function_call"]["name"]
        fuction_to_call = self._functions[function_name].fn
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
