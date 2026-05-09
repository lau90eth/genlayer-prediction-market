# Nexus V2 — Architecture

## Consensus Flow

    User calls resolve()
             │
             ▼
    ┌─────────────────┐
    │   leader_fn()   │
    │  web.get(url)   │
    │  exec_prompt()  │
    │ returns TRUE/   │
    │     FALSE       │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────────────────────┐
    │     validator_fn(leaders_res)       │
    │ 1. check isinstance(Return)         │
    │ 2. extract calldata                 │
    │ 3. web.get(url) independently       │
    │ 4. exec_prompt() independently      │
    │ 5. compare with leader result       │
    │ 6. return True only if match        │
    └────────────────┬────────────────────┘
             │
      repeated across 5 nodes
             ▼
       consensus reached
      result stored on-chain

## Key design decisions

**Why validator fetches the same URL independently?**  
In V1, `validator_fn` accepted any non-empty `gl.vm.Return`. This meant a malicious or hallucinating leader could push any result through consensus.  
In V2, each validator independently fetches the evidence source and runs its own inference — the result is only accepted if at least 4/5 nodes agree.

**Why strip null bytes?**  
GenLayer LLM output may be prefixed with `\x00` bytes in the serialized calldata. Calling `.strip().upper()` alone does not remove them. Explicit `.replace('\x00', '')` is required before string comparison or state storage.

**Why `.body.decode()` instead of direct string?**  
`gl.nondet.web.get()` returns a response object. The body must be decoded explicitly. Using `errors='replace'` prevents crashes on non-UTF8 pages.

## Contract responsibilities

| Contract            | Evidence source                        | Output                          |
|---------------------|----------------------------------------|---------------------------------|
| PredictionMarket    | Caller-supplied URL (CoinMarketCap default) | TRUE / FALSE                    |
| ParametricInsurance | FlightRadar24 for flight number        | TRUE / FALSE + payout flag      |
| DisputeResolver     | Caller-supplied URL per dispute        | PARTY_A / PARTY_B / INCONCLUSIVE|
| HelloAI             | Caller-supplied URL                    | Free-form answer (validator checks coherence) |

