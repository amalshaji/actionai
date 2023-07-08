import inspect
from typing import Any, Callable

from pydantic import create_model


def create_json_schema_for_function_input(fn: Callable) -> dict[str, Any]:
    signature = inspect.signature(fn)
    parameters = signature.parameters

    model_fields = {}

    for param in parameters.values():
        default_param = ...
        if param.default is not inspect._empty:
            default_param = param.default
        model_fields[param.name] = (param.annotation, default_param)

    DynModel = create_model(fn.__name__, **model_fields)  # type: ignore
    return DynModel.model_json_schema()
