# Runner ID Research — Bradbury Phase 1

## Problem
The official GenLayer documentation referenced a runner ID incompatible with Bradbury Phase 1. Contracts deployed with the documented runner ID returned `invalid_contract` errors.

## Method
The correct runner ID was reverse-engineered by:

1. Inspecting successful transactions on the Bradbury explorer
2. Decoding the `txDataDecoded` field from transaction receipts
3. Extracting the `# { "Depends": ... }` header from deployed contract bytecode

## Result

    py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6

## Usage
Every GenLayer Intelligent Contract must include this as the first line:

    # { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

## Status
Reported to GenLayer team. Not documented at time of discovery (May 2026).
