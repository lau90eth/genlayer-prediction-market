# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class ParametricInsurance(gl.Contract):
    flight_number: str
    payout_triggered: bool
    verdict: str
    insured: str
    premium_paid: u256
    payout_amount: u256
    settled: bool

    def __init__(self, flight_number: str):
        self.flight_number = flight_number
        self.payout_triggered = False
        self.verdict = ""
        self.insured = ""
        self.premium_paid = u256(0)
        self.payout_amount = u256(0)
        self.settled = False

    @gl.public.write
    def buy_policy(self) -> None:
        """Pay premium to insure this flight. Payout = 5x premium."""
        if self.insured != "":
            raise Exception("Policy already sold")
        amount = gl.message.value
        if amount == 0:
            raise Exception("Must send premium as value")
        self.insured = str(gl.message.sender_address)
        self.premium_paid = amount
        self.payout_amount = amount * u256(5)

    @gl.public.write
    def check_and_settle(self) -> None:
        if self.settled:
            return
        if self.insured == "":
            raise Exception("No active policy")

        fn = str(self.flight_number)
        url = f"https://www.flightradar24.com/data/flights/{fn.lower()}"

        def leader_fn() -> str:
            page = gl.nondet.web.get(url)
            snippet = page[:3000] if len(page) > 3000 else page
            prompt = (
                f"Based on this flight data:\n\n{snippet}\n\n"
                f"Was flight {fn} delayed more than 2 hours or cancelled? "
                f"Answer only TRUE or FALSE."
            )
            answer = gl.nondet.exec_prompt(prompt)
            return answer.strip().upper()

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_answer = leaders_res.value
            if leader_answer not in ("TRUE", "FALSE"):
                return False
            page = gl.nondet.web.get(url)
            snippet = page[:3000] if len(page) > 3000 else page
            prompt = (
                f"Based on this flight data:\n\n{snippet}\n\n"
                f"Was flight {fn} delayed more than 2 hours or cancelled? "
                f"Answer only TRUE or FALSE."
            )
            validator_answer = gl.nondet.exec_prompt(prompt).strip().upper()
            return validator_answer == leader_answer

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.verdict = result
        self.settled = True

        if "TRUE" in result:
            self.payout_triggered = True
            gl.message.transfer(self.insured, self.payout_amount)

    @gl.public.view
    def get_status(self) -> str:
        if not self.settled:
            return f"Policy active | Flight: {self.flight_number} | Premium: {self.premium_paid}"
        triggered = "PAYOUT TRIGGERED" if self.payout_triggered else "NO PAYOUT"
        return f"{triggered} | Verdict: {self.verdict} | Payout: {self.payout_amount}"

    @gl.public.view
    def get_insured(self) -> str:
        return self.insured
