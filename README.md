# ActionAI

A small library to run local functions using openai function calling

## Install

```shell
pip install actionai
```

## Usage

> **Note**
> A function must be fully typed and must have a docstring(one liner explanation of the function would be enough)

```python
# define a new function
def get_current_weather(location: str, unit: str = "fahrenheit"):
    """Function to get current weather for the given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return weather_info


import actionai

action = actionai.ActionAI()
action.register(get_current_weather)

response = action.prompt("What is the current weather in the north pole?")

print(response["choices"][0]["message"]["content"])
# The current weather at the North Pole is 72°F. It is sunny and windy.
```

The openai api key will be read automatically from the `OPENAI_API_KEY` environment variable. You can pass it manually as,

```python
import actionai

action = actionai.ActionAI(openai_api_key="YOUR_KEY")
```

### Adding context

Sometimes your function will have variables that needs to be set by the program.

```python
def list_todos(user: str):
    """Function to list all todos"""
    return todos[user]

action = actionai.ActionAI(context={"user": "jason"})
```

The context keys are skipped when creating json schema. The values are directly passed at the time of function calling.

### Choosing a model

By default, the completion run on the `gpt-3.5-turbo-0613` model. You can change the model using the `model` argument.

```python
import actionai

action = actionai.ActionAI(model="gpt-4")
```

You can see the complete list of supported chat completion models [here](https://platform.openai.com/docs/models/model-endpoint-compatibility)

## Demo

Running [todo example](https://github.com/amalshaji/actionai/blob/main/examples/todo.py) 👇🏻

![todo demo](https://raw.githubusercontent.com/amalshaji/actionai/main/examples/demo.svg)

For more examples, checkout the [examples](https://github.com/amalshaji/actionai/tree/main/examples) directory.
