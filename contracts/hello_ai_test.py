# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }
from genlayer import *

class HelloAITest(gl.Contract):
    last_answer: str

    def __init__(self):
        self.last_answer = ""

    @gl.public.write
    def set_answer(self, value: str):
        self.last_answer = value

    @gl.public.view
    def get_answer(self) -> str:
        return self.last_answer
