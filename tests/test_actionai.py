import pytest

import actionai


def fn_1(x: int):
    pass


def fn_2(a):
    """fn_2"""
    pass


def fn_3(a=1):
    """fn_3"""
    pass


def test_function_without_docstring_should_fail():
    action = actionai.ActionAI()
    with pytest.raises(actionai.ActionAIException) as exc_info:
        action.register(fn_1)

    assert str(exc_info.value) == "function must have a docstring"


def test_function_with_missing_annotation_should_fail():
    action = actionai.ActionAI()
    with pytest.raises(actionai.ActionAIException) as exc_info:
        action.register(fn_2)

    assert str(exc_info.value) == "parameter 'a' has missing type annotation"


def test_function_with_default_param_value_should_pass():
    action = actionai.ActionAI()
    action.register(fn_3)


def test_function_with_duplicate_name_should_fail():
    action = actionai.ActionAI()
    action.register(fn_3)
    with pytest.raises(actionai.ActionAIException) as exc_info:
        action.register(fn_3)

    assert str(exc_info.value) == "function with the same name already registered"
