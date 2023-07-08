from actionai.json_schema import create_json_schema_for_function_input


def fn_1(x: int, y: str = "4"):
    pass


def fn_2(x: int, y: str = "4", z: float = 3.14):
    pass


def test_create_json_schema_for_function_input_1():
    assert create_json_schema_for_function_input(fn_1, skip_keys=[]) == {
        "properties": {
            "x": {"title": "X", "type": "integer"},
            "y": {"default": "4", "title": "Y", "type": "string"},
        },
        "required": ["x"],
        "title": "fn_1",
        "type": "object",
    }


def test_create_json_schema_for_function_input_2():
    assert create_json_schema_for_function_input(fn_2, skip_keys=[]) == {
        "properties": {
            "x": {"title": "X", "type": "integer"},
            "y": {"default": "4", "title": "Y", "type": "string"},
            "z": {"default": 3.14, "title": "Z", "type": "number"},
        },
        "required": ["x"],
        "title": "fn_2",
        "type": "object",
    }


def test_create_json_schema_for_function_input_with_skip_keys():
    assert create_json_schema_for_function_input(fn_2, skip_keys=["y", "z"]) == {
        "properties": {
            "x": {"title": "X", "type": "integer"},
        },
        "required": ["x"],
        "title": "fn_2",
        "type": "object",
    }
