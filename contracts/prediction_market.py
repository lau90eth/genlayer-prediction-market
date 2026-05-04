# genlayer_version: 0.1.0
import genlayer as gl

class PredictionMarket(gl.Contract):
    def __init__(self, question: str):
        self.question = question
        self.resolved = False
        self.result = ""

    @gl.public.write
    def resolve(self, evidence_url: str = "") -> None:
        prompt = f"Question: {self.question}\n"
        if evidence_url:
            prompt += f"Evidence URL: {evidence_url}\n"
        prompt += "Answer with only TRUE or FALSE."
        self.result = gl.nondet.exec_prompt(prompt).strip()
        self.resolved = True

    @gl.public.view
    def get_result(self) -> str:
        return self.result

    @gl.public.view
    def is_resolved(self) -> bool:
        return self.resolved
