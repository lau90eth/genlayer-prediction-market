# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class PredictionMarket(gl.Contract):
    question: str
    evidence_url: str
    outcome: str
    resolved: bool
    total_yes: u256
    total_no: u256

    def __init__(self, question: str, evidence_url: str):
        self.question = question
        self.evidence_url = evidence_url
        self.outcome = ""
        self.resolved = False
        self.total_yes = u256(0)
        self.total_no = u256(0)

    @gl.public.write
    def place_bet(self, side: str) -> None:
        if self.resolved:
            raise Exception("Market already resolved")
        side = side.upper()
        if side not in ("YES", "NO"):
            raise Exception("side must be YES or NO")
        amount = gl.message.value
        if amount == u256(0):
            raise Exception("Must send nonzero value")
        if side == "YES":
            self.total_yes = self.total_yes + amount
        else:
            self.total_no = self.total_no + amount

    @gl.public.write
    def resolve(self) -> None:
        if self.resolved:
            return
        q = str(self.question)
        url = str(self.evidence_url)

        def leader_fn() -> str:
            page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
            prompt = (
                f"Based on the following real-world evidence:\n\n{page}\n\n"
                f"Answer only TRUE or FALSE: {q}"
            )
            raw = gl.nondet.exec_prompt(prompt)
            cleaned = raw.replace('\x00', '').strip().upper()
            if 'TRUE' in cleaned:
                return 'TRUE'
            return 'FALSE'

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_answer = leaders_res.calldata
            if not isinstance(leader_answer, str):
                return False
            leader_answer = leader_answer.replace('\x00', '').strip().upper()
            if leader_answer not in ("TRUE", "FALSE"):
                return False
            page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
            prompt = (
                f"Based on the following real-world evidence:\n\n{page}\n\n"
                f"Answer only TRUE or FALSE: {q}"
            )
            raw = gl.nondet.exec_prompt(prompt)
            validator_answer = raw.replace('\x00', '').strip().upper()
            if 'TRUE' in validator_answer:
                validator_answer = 'TRUE'
            else:
                validator_answer = 'FALSE'
            return validator_answer == leader_answer

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.outcome = result.replace('\x00', '').strip()
        self.resolved = True

    @gl.public.view
    def get_outcome(self) -> str:
        return self.outcome

    @gl.public.view
    def get_pool(self) -> str:
        return f"YES: {self.total_yes} | NO: {self.total_no}"
