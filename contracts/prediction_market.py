# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class PredictionMarket(gl.Contract):
    question: str
    outcome: str
    resolved: bool

    def __init__(self, question: str):
        self.question = question
        self.outcome = ""
        self.resolved = False

    @gl.public.write
    def resolve(self) -> None:
        if self.resolved:
            return
        q = str(self.question)
        prompt = "Answer only TRUE or FALSE: " + q

        def leader_fn() -> str:
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.outcome = result
        self.resolved = True

    @gl.public.view
    def get_outcome(self) -> str:
        return self.outcome
