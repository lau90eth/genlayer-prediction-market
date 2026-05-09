# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class HelloAI(gl.Contract):
    last_answer: str
    last_url: str

    def __init__(self):
        self.last_answer = ""
        self.last_url = ""

    @gl.public.write
    def ask(self, question: str, evidence_url: str) -> None:
        q = str(question)
        url = str(evidence_url)

        def leader_fn() -> str:
            page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
            prompt = f"Based on this evidence:\n\n{page}\n\nAnswer in one sentence: {q}"
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_answer = leaders_res.calldata
            if not isinstance(leader_answer, str):
                return False
            if len(leader_answer.strip()) < 5:
                return False
            page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
            prompt = (
                f"Based on this evidence:\n\n{page}\n\n"
                f"Does this answer make sense for the question '{q}'?\n"
                f"Answer: {leader_answer}\n"
                f"Reply only YES or NO."
            )
            check = gl.nondet.exec_prompt(prompt).strip().upper()
            return check == "YES"

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_answer = result
        self.last_url = url

    @gl.public.view
    def get_answer(self) -> str:
        return self.last_answer

    @gl.public.view
    def get_source(self) -> str:
        return self.last_url
