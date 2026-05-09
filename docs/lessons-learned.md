# Lessons Learned — Building on GenLayer Bradbury

1. Runner ID is not in the docs — reverse-engineer from explorer
2. Nondet calls must be inside run_nondet_unsafe — not directly in write methods
3. State annotations at class level are mandatory — init alone is not enough
4. web.get() returns a response object — always call .body.decode()
5. LLM output may contain null bytes — always strip \x00
6. Use .calldata not .value in validator_fn
7. Complex generic types crash at runtime — stick to str, bool, u256
8. FINALIZED timeout is common — check explorer directly, state is likely committed
9. Deploy scripts must run from node_modules directory
10. BigInt in receipts breaks JSON.stringify — use replacer function
