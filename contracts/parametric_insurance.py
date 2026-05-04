# genlayer_version: 0.1.0
import genlayer as gl

class ParametricInsurance(gl.Contract):
    def __init__(self, condition: str):
        self.condition = condition
        self.claimed = False
        self.payout = False

    @gl.public.write
    def check_and_pay(self, evidence_url: str) -> None:
        prompt = f"Insurance condition: {self.condition}\n"
        prompt += f"Evidence URL: {evidence_url}\n"
        prompt += "If the condition is MET, answer only PAYOUT. Otherwise answer only NO_PAYOUT."
        result = gl.nondet.exec_prompt(prompt).strip()
        self.payout = (result == "PAYOUT")
        self.claimed = True

    @gl.public.view
    def get_payout_status(self) -> str:
        return "PAYOUT" if self.payout else "NO_PAYOUT"

    @gl.public.view
    def is_claimed(self) -> bool:
        return self.claimed
