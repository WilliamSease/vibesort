import os
from typing_extensions import Literal
import openai
from pydantic import BaseModel
from typing import TypeVar
import ollama
import json



class VibesortResponse(BaseModel):
    sorted_array: list[int]


class VibesortRequest(BaseModel):
    array: list[int]
    order: Literal["asc", "desc"] = "asc"

Provider = Literal["openAI","ollama"]


def vibesort(array: list[int], mode:Provider = 'openAI') -> VibesortResponse:
    if mode is 'openAI':
        return structured_output(
            content=VibesortRequest(array=array).model_dump_json(),
            response_format=VibesortResponse,
        ).sorted_array
    if mode is 'ollama':
        return structured_output_local(
            content=VibesortRequest(array=array).model_dump_json(),
            response_format=VibesortResponse
        )


T = TypeVar("T", bound=BaseModel)


def structured_output(
    content: str,
    response_format: T,
    model: str = "gpt-4.1-mini",
) -> T:
    api_key = os.environ["OPENAI_API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content,
                    },
                ],
            }
        ],
        response_format=response_format,
    )
    response_model = response.choices[0].message.parsed
    return response_model


def structured_output_local(content: str,
    response_format: T,
    model: str = "qwen2.5-coder:latest", #gpt-oss:20b wasn't honoring response format
) -> T:
    content = ollama.chat(
    model=model,
    messages=[{"role": "user", "content": content}],
    stream=False,
    format=response_format.model_json_schema()).message.content
    return json.loads(content)['sorted_array']