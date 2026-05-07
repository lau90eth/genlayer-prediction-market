# Nexus — AI Consensus Infrastructure on GenLayer

**Nexus** is an AI-powered decision infrastructure built on GenLayer Bradbury Testnet. 
It deploys 4 specialized AI judges — each resolving a different type of claim using LLM consensus and real-world evidence: 
disputes between parties, insurance claims, prediction outcomes, and general Q&A. No oracles, no trusted third parties.


🌐 **Live demo**: https://lau90eth.github.io/genlayer-prediction-market/
📦 **Testnet**: GenLayer Bradbury (Phase 1)

---

## The Problem

Disputes, predictions, and insurance claims today rely on:
- Centralized arbitrators (slow, expensive, biased)
- Oracles (trusted third parties, single point of failure)
- Manual processes (days or weeks to resolve)

## The Solution

Nexus uses GenLayer's **Optimistic Democracy consensus** to resolve claims via LLM agreement across 5 independent validator nodes. No oracles. No trusted third parties. Results are final when validators agree.

---

## Contracts

| Contract | Address | Purpose |
|----------|---------|---------|
| **HelloAI** | `0xF01E92f25640426894D0315f9098011028D7090E` | On-chain Q&A via LLM consensus |
| **PredictionMarket** | `0xdef4D47E7b0255690Dd4565820B53F20DeEe0e28` | Binary outcome resolver (TRUE/FALSE) |
| **DisputeResolver** | `0x1b5e440479016B4FeE73800CB0164Af1b9C7f2AB` | Trustless AI arbitration |
| **ParametricInsurance** | `0x4f954d041756c299e8842D75a3A1cA63aecDb22F` | Automated flight delay payout |

---

## Architecture

All contracts use the `gl.vm.run_nondet_unsafe` pattern with `gl.nondet.exec_prompt`
inside `leader_fn` / `validator_fn`. This was reverse-engineered from on-chain data —
the correct runner ID and nondet pattern were not documented at time of development.

```python
def leader_fn() -> str:
    return gl.nondet.exec_prompt(prompt)

def validator_fn(leaders_res) -> bool:
    if not isinstance(leaders_res, gl.vm.Return):
        return False
    return True

result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
```

**Runner**: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

---

## How to interact

**Read contract state** (no wallet needed):
```bash
genlayer call 0xF01E92f25640426894D0315f9098011028D7090E get_answer
genlayer call 0xdef4D47E7b0255690Dd4565820B53F20DeEe0e28 get_outcome
genlayer call 0x1b5e440479016B4FeE73800CB0164Af1b9C7f2AB get_verdict
genlayer call 0x4f954d041756c299e8842D75a3A1cA63aecDb22F get_status
```

**Write transactions** (requires funded account):
```bash
genlayer write 0xF01E92f25640426894D0315f9098011028D7090E ask "Your question"
genlayer write 0xdef4D47E7b0255690Dd4565820B53F20DeEe0e28 resolve
genlayer write 0x1b5e440479016B4FeE73800CB0164Af1b9C7f2AB resolve "Claim A" "Claim B"
genlayer write 0x4f954d041756c299e8842D75a3A1cA63aecDb22F check_and_settle
```

---

## Key findings during development

Building on Bradbury required solving several undocumented issues:

- **Runner ID**: the correct pinned runner ID had to be reverse-engineered from successful transactions on the explorer — documentation referenced an incompatible version
- **Nondet pattern**: `gl.nondet.exec_prompt` cannot be called directly in a `@gl.public.write` method — it must be wrapped in `gl.vm.run_nondet_unsafe`
- **Storage type annotations**: class-level type declarations are required for state persistence — instance variables set only in `__init__` are not persisted
- **Constructor args**: passing string args via CLI requires `'"string"'` format, not `'["string"]'`

---

## Security Research

As part of this project, a DoS vulnerability was identified in the GenVM calldata decoder
(`Vec::with_capacity` with attacker-controlled size bypasses the WASM memory limiter).
Reported separately as Research & Analysis contribution.

---

## Tools

[genvm-recon](https://github.com/lau90eth/genvm-recon) — Static analyzer for GenLayer Intelligent Contracts, built while developing Nexus. Detects 9 categories of issues causing deployment failures on Bradbury.

## Built by

[lau90eth](https://github.com/lau90eth) — GenLayer Builders Program, May 2026
