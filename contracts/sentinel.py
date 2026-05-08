# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class Sentinel(gl.Contract):
    last_url: str
    last_verdict: str
    last_severity: str
    last_findings: str
    audit_count: u256

    def __init__(self):
        self.last_url = ""
        self.last_verdict = "PENDING"
        self.last_severity = "0"
        self.last_findings = ""
        self.audit_count = u256(0)

    @gl.public.write
    def audit(self, url: str) -> None:
        target_url = str(url)

        prompt_template = f"""You are an expert smart contract security auditor. 
Fetch and analyze the smart contract source code at this URL: {target_url}

Respond with EXACTLY this format (no other text):
VERDICT: SAFE or UNSAFE
SEVERITY: 0-10 (0=no issues, 10=critical vulnerabilities)
FINDINGS: one sentence summary of main security issues, or "No significant issues found" if safe"""

        def leader_fn() -> str:
            source_code = gl.nondet.web.get(target_url).body.decode('utf-8', errors='replace')[:8000]
            full_prompt = f"{prompt_template}\n\nSource code:\n{source_code}"
            return gl.nondet.exec_prompt(full_prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            result = leaders_res.calldata
            if not isinstance(result, str):
                return False
            return "VERDICT:" in result and "SEVERITY:" in result and "FINDINGS:" in result

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        verdict = "UNKNOWN"
        severity = "0"
        findings = ""

        for line in result.split('\n'):
            line = line.strip()
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            elif line.startswith("SEVERITY:"):
                severity = line.replace("SEVERITY:", "").strip()
            elif line.startswith("FINDINGS:"):
                findings = line.replace("FINDINGS:", "").strip()

        self.last_url = target_url
        self.last_verdict = verdict
        self.last_severity = severity
        self.last_findings = findings
        self.audit_count = self.audit_count + u256(1)

    @gl.public.view
    def get_audit(self) -> str:
        return f"URL: {self.last_url} | VERDICT: {self.last_verdict} | SEVERITY: {self.last_severity}/10 | FINDINGS: {self.last_findings}"

    @gl.public.view
    def get_verdict(self) -> str:
        return self.last_verdict

    @gl.public.view
    def get_severity(self) -> str:
        return self.last_severity

    @gl.public.view
    def get_findings(self) -> str:
        return self.last_findings

    @gl.public.view
    def get_count(self) -> str:
        return str(self.audit_count)
