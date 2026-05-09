# genvm-recon — Static Analyzer for GenLayer Intelligent Contracts

Built while developing Nexus. Detects 9 categories of issues that cause deployment or runtime failures on Bradbury Phase 1.

## Checks

1. Missing class-level type annotations (state not persisted)
2. Direct `gl.nondet.exec_prompt()` outside `run_nondet_unsafe`
3. Complex generic types (`TreeMap[str, tuple[...]]`)
4. Missing `.body.decode()` on web responses
5. Use of `.value` instead of `.calldata` in validator_fn
6. Null byte not stripped from LLM output
7. BigInt serialization issues in deploy scripts
8. Missing `# { "Depends": ... }` runner header
9. `gl.message.value` compared to plain `0` instead of `u256(0)`

## Usage

```bash
python genvm-recon.py contracts/my_contract.py
```
