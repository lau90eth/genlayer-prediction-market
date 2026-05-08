# Nexus — AI Consensus Infrastructure on GenLayer

**Nexus** is an AI-powered decision infrastructure built on GenLayer Bradbury Testnet. It deploys 4 specialized AI judges — each resolving a different type of claim using LLM consensus and real-world evidence: disputes between parties, insurance claims, prediction outcomes, and general Q&A. No oracles, no trusted third parties.

🌐 **Live demo (V2):** https://lau90eth.github.io/genlayer-prediction-market/nexus_v2.html
🌐 **Live demo (V1):** https://lau90eth.github.io/genlayer-prediction-market/
🔗 **Testnet:** GenLayer Bradbury (Phase 1)

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

### V2 — Evidence-backed validator consensus (current)

| Contract              | Address                                    | Purpose |
|-----------------------|--------------------------------------------|-------|
| HelloAI               | 0x527D6B123cd2411BE5637bDA17b9d874D85Fe838 | Evidence-grounded Q&A |
| PredictionMarket      | 0x381017E9623982a9D8d067b4cAaAAb6B090c0f18 | Binary outcome resolver with real evidence |
| DisputeResolver       | 0x06f625b012d2822Aa69E2Bd542DdcdE574DCCd9f | Trustless AI arbitration with web evidence |
| ParametricInsurance   | 0x562F85Fbd585F98ba0D8B160f01CE20333f2a298 | Flight delay payout via live data |

### V1 — Initial deployment

| Contract              | Address                                    | Purpose |
|-----------------------|--------------------------------------------|-------|
| HelloAI               | 0xF01E92f25640426894D0315f9098011028D7090E | On-chain Q&A via LLM consensus |
| PredictionMarket      | 0xdef4D47E7b0255690Dd4565820B53F20DeEe0e28 | Binary outcome resolver (TRUE/FALSE) |
| DisputeResolver       | 0x1b5e440479016B4FeE73800CB0164Af1b9C7f2AB | Trustless AI arbitration |
| ParametricInsurance   | 0x4f954d041756c299e8842D75a3A1cA63aecDb22F | Automated flight delay payout |

---

## What changed in V2

Following staff feedback ("validators accept any leader response, contracts do not fetch real-world evidence"):

- **Independent validator consensus**: every validator independently fetches the evidence URL and runs its own LLM inference — result accepted only if validator and leader agree
- **Real-world evidence fetching**: all contracts use `gl.nondet.web.get()` before reasoning
- **Real market structure**: PredictionMarket tracks YES/NO pools on-chain; ParametricInsurance tracks policy state and payout trigger

---

## Architecture

All contracts use `gl.vm.run_nondet_unsafe` with `gl.nondet.web.get()` + `gl.nondet.exec_prompt` inside `leader_fn` / `validator_fn`.

    def leader_fn() -> str:
        page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]
        return gl.nondet.exec_prompt(prompt).strip().upper()

    def validator_fn(leaders_res) -> bool:
        leader_answer = leaders_res.calldata
        # fetch independently and compare
        validator_answer = gl.nondet.exec_prompt(prompt).strip().upper()
        return validator_answer == leader_answer

**Runner:** `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

---

## How to interact

**Read contract state** (no wallet needed):

    genlayer call 0x527D6B123cd2411BE5637bDA17b9d874D85Fe838 get_answer
    genlayer call 0x381017E9623982a9D8d067b4cAaAAb6B090c0f18 get_outcome
    genlayer call 0x06f625b012d2822Aa69E2Bd542DdcdE574DCCd9f get_verdict
    genlayer call 0x562F85Fbd585F98ba0D8B160f01CE20333f2a298 get_status

**Write transactions** (requires funded account):

    genlayer write 0x527D6B123cd2411BE5637bDA17b9d874D85Fe838 ask "Your question" "https://evidence-url"
    genlayer write 0x381017E9623982a9D8d067b4cAaAAb6B090c0f18 resolve
    genlayer write 0x06f625b012d2822Aa69E2Bd542DdcdE574DCCd9f resolve "Claim A" "Claim B" "https://evidence-url"
    genlayer write 0x562F85Fbd585F98ba0D8B160f01CE20333f2a298 check_and_settle

---

## Key findings during development

- **Runner ID**: reverse-engineered from successful transactions — documentation referenced an incompatible version
- **Nondet pattern**: `gl.nondet.exec_prompt` must be wrapped in `gl.vm.run_nondet_unsafe`
- **Storage type annotations**: class-level type declarations required for state persistence
- **Null bytes**: GenLayer LLM output may contain `\x00` prefix — must be stripped before storing state
- **Constructor args**: passing string args via CLI requires `'"string"'` format

---

## Security Research

A DoS vulnerability was identified in the GenVM calldata decoder (`Vec::with_capacity` with attacker-controlled size bypasses the WASM memory limiter). Reported separately as Research & Analysis contribution.

---

## Tools

[genvm-recon](https://github.com/lau90eth/genvm-recon) — Static analyzer for GenLayer Intelligent Contracts, built while developing Nexus.

## Built by

[lau90eth](https://github.com/lau90eth) — GenLayer Builders Program, May 2026
