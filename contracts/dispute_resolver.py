# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class DisputeResolver(gl.Contract):
    last_verdict: str

    def __init__(self):
        self.last_verdict = ""

    @gl.public.write
    def resolve(self, claim_a: str, claim_b: str) -> None:
        a = str(claim_a)
        b = str(claim_b)
        prompt = f"You are an impartial arbitrator. Party A claims: {a}. Party B claims: {b}. Give a fair one-sentence verdict."

        def leader_fn() -> str:
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_verdict = result

    @gl.public.view
    def get_verdict(self) -> str:
        return self.last_verdict
