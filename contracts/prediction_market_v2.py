# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class PredictionMarket(gl.Contract):
    question: str
    outcome: str
    resolved: bool
    evidence_url: str
    total_yes: u256
    total_no: u256
    bets: TreeMap[str, tuple[str, u256]]  # addr -> (side, amount)

    def __init__(self, question: str, evidence_url: str):
        self.question = question
        self.evidence_url = evidence_url
        self.outcome = ""
        self.resolved = False
        self.total_yes = u256(0)
        self.total_no = u256(0)
        self.bets = TreeMap()

    @gl.public.write
    def place_bet(self, side: str) -> None:
        """Place a bet. side must be 'YES' or 'NO'. Value sent = bet amount."""
        if self.resolved:
            raise Exception("Market already resolved")
        side = side.upper()
        if side not in ("YES", "NO"):
            raise Exception("side must be YES or NO")
        amount = gl.message.value
        if amount == 0:
            raise Exception("Must send nonzero value")
        caller = str(gl.message.sender_address)
        self.bets[caller] = (side, amount)
        if side == "YES":
            self.total_yes += amount
        else:
            self.total_no += amount

    @gl.public.write
    def resolve(self) -> None:
        if self.resolved:
            return

        q = str(self.question)
        url = str(self.evidence_url)

        def leader_fn() -> str:
            # Fetch real-world evidence from the provided URL
            page = gl.nondet.web.get(url)
            # Truncate to avoid token limits
            snippet = page[:3000] if len(page) > 3000 else page
            prompt = (
                f"Based on the following real-world evidence:\n\n{snippet}\n\n"
                f"Answer only TRUE or FALSE: {q}"
            )
            answer = gl.nondet.exec_prompt(prompt)
            return answer.strip().upper()

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_answer = leaders_res.value
            if leader_answer not in ("TRUE", "FALSE"):
                return False
            # Validator independently fetches the same URL and reasons
            page = gl.nondet.web.get(url)
            snippet = page[:3000] if len(page) > 3000 else page
            prompt = (
                f"Based on the following real-world evidence:\n\n{snippet}\n\n"
                f"Answer only TRUE or FALSE: {q}"
            )
            validator_answer = gl.nondet.exec_prompt(prompt).strip().upper()
            # Accept if validator reaches same conclusion
            return validator_answer == leader_answer

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.outcome = result
        self.resolved = True

    @gl.public.view
    def get_outcome(self) -> str:
        return self.outcome

    @gl.public.view
    def get_pool(self) -> str:
        return f"YES: {self.total_yes} | NO: {self.total_no}"

    @gl.public.view
    def get_bet(self, addr: str) -> str:
        if addr not in self.bets:
            return "no bet"
        side, amount = self.bets[addr]
        return f"{side}: {amount}"
