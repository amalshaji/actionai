import inspect
from typing import Any, Callable, Dict, List

from pydantic import create_model

from actionai.exceptions import ActionAIException


def create_json_schema_for_function_input(
    fn: Callable, skip_keys: List[str]
) -> Dict[str, Any]:
    """Create json schema for a function's input

    Args:
        fn (Callable): The function
        skip_keys (List[str]): The arguments to skip (context keys)

    Returns:
        Dict[str, Any]: The json schema
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

        annotation = param.annotation
        if annotation is param.empty and default_param is not ...:
            annotation = type(default_param)
        if annotation is param.empty:
            raise ActionAIException(
                f"parameter '{param.name}' has missing type annotation"
            )

        model_fields[param.name] = (annotation, default_param)

    DynModel = create_model(fn.__name__, **model_fields)  # type: ignore
    return DynModel.model_json_schema()
