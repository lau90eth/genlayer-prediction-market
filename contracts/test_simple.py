# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }
from genlayer import *

class TestSimple:
    def __init__(self):
        self.value = "hello"
    
    @gl.public.view
    def get_value(self):
        return self.value
