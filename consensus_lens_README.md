# ConsensusLens

Live benchmark dashboard for GenLayer Intelligent Contracts on Bradbury Testnet.

## What it does

ConsensusLens fetches real transaction data from the Bradbury explorer and shows:
- Consensus rate per contract
- Disagreement frequency (UNDETERMINED transactions)
- Average execution time
- Execution timeline visualization
- Full transaction history with links to explorer

## Live demo

https://lau90eth.github.io/genlayer-prediction-market/consensus_lens.html

## Contracts analyzed

| Contract | Address | Consensus Rate |
|---|---|---|
| HelloAI | 0x527D6B123cd2411BE5637bDA17b9d874D85Fe838 | 100% |
| Sentinel | 0xba13012389EcDF77825956d3647525D8a96B1269 | 100% |
| PredictionMarket | 0x381017E9623982a9D8d067b4cAaAAb6B090c0f18 | 100% |
| DisputeResolver | 0x23E4AC68D7F32354877d54751B83eB7f28Ea794B | 100% |

## On-chain registry

ConsensusLens also includes an on-chain benchmark registry contract that stores run metadata permanently on Bradbury.

Registry: 0x2122Daafc5c291Ce802294724B0434a0F9E2285c

## Complementary to bradbury-gym

bradbury-gym benchmarks validator node performance. ConsensusLens benchmarks Intelligent Contract behavior — consensus stability, execution time variance, and disagreement patterns.

## Tech

- Frontend: vanilla HTML/JS, reads live from Bradbury explorer API
- Registry: GenLayer Intelligent Contract (Python)
- No wallet required to view data
