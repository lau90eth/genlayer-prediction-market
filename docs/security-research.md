# Security Research — GenVM DoS Vulnerability

## Finding
A DoS vulnerability was identified in the GenVM calldata decoder.

`Vec::with_capacity` is called with an attacker-controlled size value from the calldata, bypassing the WASM memory limiter. A malicious caller can trigger an OOM condition in the validator node process.

## Impact
- Validator node crash on malformed calldata
- Potential network-level DoS if majority of validators affected simultaneously

## Reported
Reported separately as Research & Analysis contribution to the GenLayer Builders Program.
