# ActionAI

A small library to run local functions using openai function calling

## Install

```shell
pip install actionai
```

## Usage

```python
# define a new function
# example from openai functions examples
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

> **Warning**
> A function must be fully typed and must have a docstring(one liner explanation of the function is enough)

## Demo

Running [todo example](/examples/todo.py) 👇🏻

![todo demo](/examples/demo.svg)

For more examples, checkout the [examples](/examples/) directory.
