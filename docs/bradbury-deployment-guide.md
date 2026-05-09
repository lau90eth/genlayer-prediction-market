# Bradbury Deployment Guide (Updated V2)

## Environment

- Node.js 18+
- genlayer-js installed locally (not globally)
- All deploy scripts must run from the directory containing node_modules

## Common errors and fixes

### ERR_MODULE_NOT_FOUND
Run deploy scripts from the directory where genlayer-js is installed:
```bash
cd ~/gl-write-test && node deploy.mjs
```

### ACCEPTED (ERROR) on explorer
Usually caused by:
- Complex generic types in state annotations
- Missing runner ID header
- `gl.nondet.exec_prompt` called outside `run_nondet_unsafe`

### TypeError: Cannot read properties of undefined (reading contract_address)
Receipt structure varies. Use:
```javascript
console.log(JSON.stringify(receipt, (_, v) => typeof v === 'bigint' ? v.toString() : v, 2));
```

### Timed out waiting for FINALIZED
Transaction may still succeed. Check explorer with the TX hash and read state directly.

### sed unterminated s command
Private keys containing `/` break sed. Use a placeholder string without special characters, or set the key directly in the script.

## Deploy template

```javascript
import { createClient } from 'genlayer-js';
import { testnetBradbury } from 'genlayer-js/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { readFileSync } from 'fs';

const account = privateKeyToAccount('YOUR_PRIVATE_KEY');
const client = createClient({ chain: testnetBradbury, account });
const code = readFileSync('./contract.py', 'utf8');

const hash = await client.deployContract({ code, args: [] });
console.log('TX:', hash);

const receipt = await client.waitForTransactionReceipt({
  hash, status: 'ACCEPTED', retries: 60, interval: 5000
});
console.log(JSON.stringify(receipt, (_, v) => typeof v === 'bigint' ? v.toString() : v, 2));
```
