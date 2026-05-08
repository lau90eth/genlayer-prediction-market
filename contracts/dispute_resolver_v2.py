# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class DisputeResolver(gl.Contract):
    last_verdict: str
    party_a: str
    party_b: str
    stake_a: u256
    stake_b: u256
    settled: bool

    def __init__(self):
        self.last_verdict = ""
        self.party_a = ""
        self.party_b = ""
        self.stake_a = u256(0)
        self.stake_b = u256(0)
        self.settled = False

    @gl.public.write
    def file_claim(self, side: str) -> None:
        """side = 'A' or 'B'. Send stake as value."""
        if self.settled:
            raise Exception("Dispute already settled")
        side = side.upper()
        amount = gl.message.value
        if amount == 0:
            raise Exception("Must send stake")
        caller = str(gl.message.sender_address)
        if side == "A":
            self.party_a = caller
            self.stake_a = amount
        elif side == "B":
            self.party_b = caller
            self.stake_b = amount
        else:
            raise Exception("side must be A or B")

    @gl.public.write
    def resolve(self, claim_a: str, claim_b: str, evidence_url: str) -> None:
        if self.settled:
            return

        a = str(claim_a)
        b = str(claim_b)
        url = str(evidence_url)

        def leader_fn() -> str:
            page = gl.nondet.web.get(url)
            snippet = page[:3000] if len(page) > 3000 else page
            prompt = (
                f"Real-world evidence:\n\n{snippet}\n\n"
                f"Party A claims: {a}\n"
                f"Party B claims: {b}\n"
                f"Based only on the evidence, who is correct? "
                f"Answer only: PARTY_A or PARTY_B or INCONCLUSIVE"
            )
            return gl.nondet.exec_prompt(prompt).strip().upper()

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_answer = leaders_res.value
            if leader_answer not in ("PARTY_A", "PARTY_B", "INCONCLUSIVE"):
                return False
            page = gl.nondet.web.get(url)
            snippet = page[:3000] if len(page) > 3000 else page
            prompt = (
                f"Real-world evidence:\n\n{snippet}\n\n"
                f"Party A claims: {a}\n"
                f"Party B claims: {b}\n"
                f"Based only on the evidence, who is correct? "
                f"Answer only: PARTY_A or PARTY_B or INCONCLUSIVE"
            )
            validator_answer = gl.nondet.exec_prompt(prompt).strip().upper()
            return validator_answer == leader_answer

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_verdict = result
        self.settled = True

        total = self.stake_a + self.stake_b
        if result == "PARTY_A" and self.party_a != "":
            gl.message.transfer(self.party_a, total)
        elif result == "PARTY_B" and self.party_b != "":
            gl.message.transfer(self.party_b, total)

    @gl.public.view
    def get_verdict(self) -> str:
        return self.last_verdict

    @gl.public.view
    def get_stakes(self) -> str:
        return f"A: {self.stake_a} | B: {self.stake_b}"
