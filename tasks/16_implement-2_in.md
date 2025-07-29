In `tasks/15_implement_out.md` there was an issue with the agent. I though we'd corrected this. The wrong python library is being used.

`google.generativeai` is deprecated. `google-genai`  PyPI version 1.27.0  is the library we're supposed to be using.

```
pip install google-genai
```

Below are some snippets from the docs. I retrived them from here: https://pypi.org/project/google-genai/

You can also search the Context7 docs - which are LLM Model friendly docs and instructions. You can replace `{{SEARCH TOPIC HERE}}` with a topic to filter the docs on - to get more specific information about a topic.

https://context7.com/context7/googleapis_github_io-python-genai/llms.txt?topic={{SEARCH TOPIC HERE}}

# Docs

```
from google import genai
from google.genai import types

# Only run this block for Gemini Developer API
client = genai.Client(api_key='GEMINI_API_KEY')

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)
```

## How to structure contents argument for generate_content
The SDK always converts the inputs to the contents argument into list[types.Content]. The following shows some common ways to provide your inputs.

Provide a list[types.Content]
This is the canonical way to provide contents, SDK will not do any conversion.

Provide a types.Content instance

```
from google.genai import types

contents = types.Content(
  role='user',
  parts=[types.Part.from_text(text='Why is the sky blue?')]
)
```

SDK converts this to

```
[
  types.Content(
    role='user',
    parts=[types.Part.from_text(text='Why is the sky blue?')]
  )
]
```

## Provide a function call part

```
from google.genai import types

contents = types.Part.from_function_call(
  name='get_weather_by_location',
  args={'location': 'Boston'}
)
```

The SDK converts a function call part to a content with a model role:

```
[
  types.ModelContent(
    parts=[
      types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'Boston'}
      )
    ]
  )
]
```

## System Instructions and Other Configs

The output of the model can be influenced by several optional settings available in generate_content's config parameter. For example, increasing max_output_tokens is essential for longer model responses. To make a model more deterministic, lowering the temperature parameter reduces randomness, with values near 0 minimizing variability. Capabilities and parameter defaults for each model is shown in the Vertex AI docs and Gemini API docs respectively.

```
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='high',
    config=types.GenerateContentConfig(
        system_instruction='I say high, you say low',
        max_output_tokens=3,
        temperature=0.3,
    ),
)
print(response.text)
```

## Function Calling

### Automatic Python function Support

You can pass a Python function directly and it will be automatically called and responded by default.

```
from google.genai import types

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
    """
    return 'sunny'


response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(tools=[get_current_weather]),
)

print(response.text)
```

### Disabling automatic function calling

If you pass in a python function as a tool directly, and do not want automatic function calling, you can disable automatic function calling as follows:

```
from google.genai import types

response = client.models.generate_content(
  model='gemini-2.0-flash-001',
  contents='What is the weather like in Boston?',
  config=types.GenerateContentConfig(
    tools=[get_current_weather],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
      disable=True
    ),
  ),
)
```

With automatic function calling disabled, you will get a list of function call parts in the response:

`function_calls: Optional[List[types.FunctionCall]] = response.function_calls`

### Manually declare and invoke a function for function calling

If you don't want to use the automatic function support, you can manually declare the function and invoke it.

The following example shows how to declare a function and pass it as a tool. Then you will receive a function call part in the response.

```
from google.genai import types

function = types.FunctionDeclaration(
    name='get_current_weather',
    description='Get the current weather in a given location',
    parameters_json_schema={
        'type': 'object',
        'properties': {
            'location': {
                'type': 'string',
                'description': 'The city and state, e.g. San Francisco, CA',
            }
        },
        'required': ['location'],
    },
)

tool = types.Tool(function_declarations=[function])

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(tools=[tool]),
)

print(response.function_calls[0])
```

After you receive the function call part from the model, you can invoke the function and get the function response. And then you can pass the function response to the model. The following example shows how to do it for a simple function invocation.

```
from google.genai import types

user_prompt_content = types.Content(
    role='user',
    parts=[types.Part.from_text(text='What is the weather like in Boston?')],
)
function_call_part = response.function_calls[0]
function_call_content = response.candidates[0].content


try:
    function_result = get_current_weather(
        **function_call_part.function_call.args
    )
    function_response = {'result': function_result}
except (
    Exception
) as e:  # instead of raising the exception, you can let the model handle it
    function_response = {'error': str(e)}


function_response_part = types.Part.from_function_response(
    name=function_call_part.name,
    response=function_response,
)
function_response_content = types.Content(
    role='tool', parts=[function_response_part]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[
        user_prompt_content,
        function_call_content,
        function_response_content,
    ],
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)

print(response.text)
```

### Function calling with ANY tools config mode

If you configure function calling mode to be ANY, then the model will always return function call parts. If you also pass a python function as a tool, by default the SDK will perform automatic function calling until the remote calls exceed the maximum remote call for automatic function calling (default to 10 times).

If you'd like to disable automatic function calling in ANY mode:

```
from google.genai import types

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    ),
)
```

If you'd like to set x number of automatic function call turns, you can configure the maximum remote calls to be x + 1. Assuming you prefer 1 turn for automatic function calling.

```
from google.genai import types

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=2
        ),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    ),
)
```
