# GenLayer AI Ecosystem

AI-powered contracts on GenLayer Testnet Bradbury (Phase 1).

## What it does

Resolves binary outcomes, disputes, and Q&A via **LLM consensus** using real-time web evidence. No oracles, no trusted third parties.

## Contracts

| Contract | Address | Description |
|---|---|---|
| HelloAI | `0x0A09E80615C039dCBEE10dd52f4e2F7DAdBb4465` | Basic AI Q&A |
| PredictionMarket | `0x36C4b7fD7494fac52d87B303B9B7065D4AfC1762` | Binary outcome resolver |
| DisputeResolver | `0xB05b345816848DB8065317d15873EB036dF71b00` | Trustless AI arbitration |

## Tech stack

- Language: Python (Intelligent Contracts)
- Network: GenLayer Bradbury Testnet
- CLI: GenLayer v0.39.0

## Deploy

```bash
genlayer deploy --contract contracts/prediction_market.py --args 'Will Bitcoin reach 100k in 2026?'
genlayer deploy --contract contracts/dispute_resolver.py --args 'Online purchase refund dispute'
