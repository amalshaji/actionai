import inspect
from typing import Any, Callable

from pydantic import create_model


def create_json_schema_for_function_input(
    fn: Callable, skip_keys: list[str]
) -> dict[str, Any]:
    """Create json schema for a function's input

    Args:
        fn (Callable): The function
        skip_keys (list[str]): The arguments to skip (context keys)

    Returns:
        dict[str, Any]: The json schema
    """
    signature = inspect.signature(fn)
    parameters = signature.parameters

    model_fields = {}

    for param in parameters.values():
        if param.name in skip_keys:
            continue
        default_param = ...
        if param.default is not inspect._empty:
            default_param = param.default
        model_fields[param.name] = (param.annotation, default_param)

    DynModel = create_model(fn.__name__, **model_fields)  # type: ignore
    return DynModel.model_json_schema()
