# GenLayer AI Ecosystem

AI-powered contracts on GenLayer Testnet Bradbury (Phase 1).

## Contracts

| Contract | Address | Description |
|---|---|---|
| HelloAI | `0xF01E92f25640426894D0315f9098011028D7090E` | Basic AI Q&A |
| PredictionMarket | `0xdef4D47E7b0255690Dd4565820B53F20DeEe0e28` | Binary outcome resolver |
| DisputeResolver | `0x1b5e440479016B4FeE73800CB0164Af1b9C7f2AB` | Trustless AI arbitration |
| ParametricInsurance | `0x4f954d041756c299e8842D75a3A1cA63aecDb22F` | Flight delay insurance |

## Tech stack

- Language: Python (Intelligent Contracts)
- Network: GenLayer Bradbury Testnet
- CLI: GenLayer v0.39.0

## Deploy

```bash
genlayer deploy --contract contracts/prediction_market.py --args '"Will Bitcoin reach 100k in 2026?"'
genlayer deploy --contract contracts/dispute_resolver.py
genlayer deploy --contract contracts/parametric_insurance.py --args '"AZ1234"'
