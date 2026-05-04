# GenLayer Prediction Market

AI-powered prediction market built on **GenLayer Testnet Bradbury (Phase 1)**.

## What it does

Resolves binary outcomes (TRUE/FALSE) via **LLM consensus** using real-time web evidence. No oracles, no trusted third parties.

## Contracts

| Contract | Address | Description |
|---|---|---|
| `HelloAI` | `0x0A09E80615C039dCBEE10dd52f4e2F7DAdBb4465` | Basic AI Q&A |
| `PredictionMarket` | `0x36C4b7fD7494fac52d87B303B9B7065D4AfC1762` | Binary market resolved by AI validators |

## Tech stack

- **Language:** Python (Intelligent Contracts)
- **Network:** GenLayer Bradbury Testnet
- **CLI:** GenLayer v0.39.0

## Deploy

```bash
genlayer deploy --contract contracts/prediction_market.py --args 'Will Bitcoin reach 100k in 2026?'

## Contracts (Updated)

| Contract | Address | Description |
|---|---|---|
| `HelloAI` | `0x0A09E80615C039dCBEE10dd52f4e2F7DAdBb4465` | Basic AI Q&A |
| `PredictionMarket` | `0x36C4b7fD7494fac52d87B303B9B7065D4AfC1762` | Binary market resolver |
| `DisputeResolver` | `0xB05b345816848DB8065317d15873EB036dF71b00` | Trustless AI arbitration |

## DisputeResolver

Decentralized dispute resolution using LLM consensus. Judges claims with web evidence — no human arbitrator needed.
