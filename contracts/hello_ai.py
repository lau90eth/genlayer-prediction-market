# genlayer_version: 0.1.0
import genlayer as gl

class HelloAI(gl.Contract):
    def __init__(self):
        self.last_answer = ""

    @gl.public.write
    def ask(self, question: str) -> None:
        result = gl.nondet.exec_prompt(f"Answer briefly: {question}")
        self.last_answer = result.strip()

    @gl.public.view
    def get_answer(self) -> str:
        return self.last_answer
