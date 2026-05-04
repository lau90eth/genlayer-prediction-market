# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class ParametricInsurance(gl.Contract):
    flight_number: str
    payout_triggered: bool
    verdict: str

    def __init__(self, flight_number: str):
        self.flight_number = flight_number
        self.payout_triggered = False
        self.verdict = ""

    @gl.public.write
    def check_and_settle(self) -> None:
        if self.payout_triggered:
            return
        fn = str(self.flight_number)
        prompt = f"Was flight {fn} delayed more than 2 hours or cancelled recently? Answer only TRUE or FALSE."

        def leader_fn() -> str:
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.verdict = result
        if "TRUE" in result.upper():
            self.payout_triggered = True

    @gl.public.view
    def get_status(self) -> str:
        return self.verdict
