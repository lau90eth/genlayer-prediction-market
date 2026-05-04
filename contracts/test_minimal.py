# { "Depends": "python:latest" }
import genlayer as gl

class Test(gl.Contract):
    def __init__(self):
        self.value = "hello"
