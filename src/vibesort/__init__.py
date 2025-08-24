from . import ai
from typing import Literal

Provider = Literal["openAI","ollama"]

def vibesort(arr: list[int], mode:Provider = 'openAI') -> list[int]:
    return ai.vibesort(arr,mode)
