# Finding: Null byte prefix in GenLayer LLM output

## Summary
`gl.nondet.exec_prompt()` on GenLayer Bradbury Phase 1 may return output prefixed with one or more `\x00` (null) bytes. This causes silent failures when comparing strings or storing state.

## Observed behavior
Explorer shows: `\u0000,FALSE`
Expected: `FALSE`

## Impact
- String comparison `result == "FALSE"` returns `False`
- `get_outcome()` returns empty string despite resolved market
- `validator_fn` rejects valid leader results if checking exact match

## Fix
```python
raw = gl.nondet.exec_prompt(prompt)
cleaned = raw.replace('\x00', '').strip().upper()
if 'TRUE' in cleaned:
    return 'TRUE'
return 'FALSE'
```
Also strip on storage:
```python
self.outcome = result.replace('\x00', '').strip()
```

## Affected contracts
All contracts using `gl.nondet.exec_prompt()` on Bradbury Phase 1.

## Status
Fixed in Nexus V2. Reported to GenLayer team.
