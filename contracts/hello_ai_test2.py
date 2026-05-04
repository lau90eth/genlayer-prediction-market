# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }
from genlayer import *

class HelloAITest2(gl.Contract):
    value: str

    def __init__(self):
        self.value = ""

    @gl.public.write
    def set_test(self):
        self.value = "TEST123"
        return self.value

    @gl.public.view
    def get_value(self) -> str:
        return self.value
