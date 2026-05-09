# Contributing to Nexus

## Setup

```bash
git clone https://github.com/lau90eth/genlayer-prediction-market
cd genlayer-prediction-market
```

## Contract development

Contracts live in `contracts/`. Each file is a self-contained GenLayer Intelligent Contract.

Before deploying, verify:
- Class-level type annotations present for all state variables
- No complex generic types (`tuple`, parameterized `TreeMap`)
- All LLM output sanitized with `.replace('\x00', '').strip()`
- `gl.nondet.web.get()` calls use `.body.decode('utf-8', errors='replace')`
- `validator_fn` uses `leaders_res.calldata`, not `.value`

## Testing on Bradbury

Deploy scripts are in `~/gl-write-test/` (requires local `genlayer-js` install).

Read state:
```bash
node read_v2.mjs
```

## Reporting issues

Open a GitHub issue with:
- Contract name and address
- Transaction hash
- Expected vs actual behavior
- GenLayer explorer link
