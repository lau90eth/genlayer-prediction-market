# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class DisputeResolver(gl.Contract):
    last_verdict: str
    settled: bool

    def __init__(self):
        self.last_verdict = ""
        self.settled = False

    @gl.public.write
    def resolve(self, claim_a: str, claim_b: str, evidence_url: str) -> None:
        if self.settled:
            return
        a = str(claim_a)
        b = str(claim_b)
        url = str(evidence_url)

        def leader_fn() -> str:
            page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
            prompt = (
                f"Real-world evidence:\n\n{page}\n\n"
                f"Party A claims: {a}\n"
                f"Party B claims: {b}\n"
                f"Based only on the evidence, who is correct? "
                f"Answer only: PARTY_A or PARTY_B or INCONCLUSIVE"
            )
            raw = gl.nondet.exec_prompt(prompt)
            cleaned = raw.replace('\x00', '').strip().upper()
            if 'PARTY_A' in cleaned:
                return 'PARTY_A'
            elif 'PARTY_B' in cleaned:
                return 'PARTY_B'
            return 'INCONCLUSIVE'

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_answer = leaders_res.calldata
            if not isinstance(leader_answer, str):
                return False
            leader_answer = leader_answer.replace('\x00', '').strip().upper()
            if leader_answer not in ("PARTY_A", "PARTY_B", "INCONCLUSIVE"):
                return False
            page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
            prompt = (
                f"Real-world evidence:\n\n{page}\n\n"
                f"Party A claims: {a}\n"
                f"Party B claims: {b}\n"
                f"Based only on the evidence, who is correct? "
                f"Answer only: PARTY_A or PARTY_B or INCONCLUSIVE"
            )
            raw = gl.nondet.exec_prompt(prompt)
            cleaned = raw.replace('\x00', '').strip().upper()
            if 'PARTY_A' in cleaned:
                validator_answer = 'PARTY_A'
            elif 'PARTY_B' in cleaned:
                validator_answer = 'PARTY_B'
            else:
                validator_answer = 'INCONCLUSIVE'
            return validator_answer == leader_answer

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_verdict = result.replace('\x00', '').strip()
        self.settled = True

    @gl.public.view
    def get_verdict(self) -> str:
        return self.last_verdict
