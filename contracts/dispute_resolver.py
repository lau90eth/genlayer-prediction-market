# genlayer_version: 0.1.0
import genlayer as gl

class DisputeResolver(gl.Contract):
    def __init__(self, topic: str):
        self.topic = topic
        self.verdict = ""
        self.resolved = False

    @gl.public.write
    def submit_evidence(self, claim: str, evidence_url: str) -> None:
        prompt = f"Topic: {self.topic}\nClaim: {claim}\nEvidence: {evidence_url}\n"
        prompt += "You are an impartial judge. Answer VALID or INVALID."
        self.verdict = gl.nondet.exec_prompt(prompt).strip()
        self.resolved = True

    @gl.public.view
    def get_verdict(self) -> str:
        return self.verdict

    @gl.public.view
    def is_resolved(self) -> bool:
        return self.resolved
