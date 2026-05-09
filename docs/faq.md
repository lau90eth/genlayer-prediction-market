# FAQ

**Why GenLayer instead of Chainlink or UMA?**
GenLayer validators run LLM inference natively — no oracle network, no bond/dispute game, no off-chain relayer. The consensus is enforced by the VM itself.

**Why 5 validators?**
Bradbury Phase 1 default. Results finalize when 4/5 nodes agree (optimistic democracy).

**Can the evidence URL be manipulated?**
The URL is set at deploy time (PredictionMarket, ParametricInsurance) or per call (DisputeResolver, HelloAI). A malicious caller supplying a fake URL would only affect their own dispute. Future versions could use a whitelist of trusted sources.

**What happens if validators disagree?**
`gl.vm.run_nondet_unsafe` retries. Persistent disagreement results in the transaction failing.

**Why are there V1 and V2 contracts?**
V1 was the initial hackathon submission. V2 addresses staff feedback: real evidence fetching, independent validator consensus, and on-chain market state.

**Why does the explorer show \u0000,FALSE?**
This is a GenLayer serialization artifact. The null byte prefix is stripped by the contract before storing state. `get_outcome()` returns clean `FALSE`.
