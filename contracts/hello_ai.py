# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class HelloAI(gl.Contract):
    last_answer: str

    def __init__(self):
        self.last_answer = ""

    @gl.public.write
    def ask(self, question: str) -> None:
        prompt = "Answer in one sentence: " + question

        def leader_fn() -> str:
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True  # accetta qualsiasi risposta non-vuota

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_answer = result

    @gl.public.view
    def get_answer(self) -> str:
        return self.last_answer
