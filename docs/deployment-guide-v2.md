# Nexus V2 Deployment Guide — GenLayer Bradbury

## Prerequisites

- Node.js 18+
- `genlayer-js` installed in working directory
- Funded account on Bradbury testnet

## Critical fixes discovered during V1 deployment

### 1. Null bytes in LLM output
GenLayer may return `\x00,TRUE` instead of `TRUE`. Always sanitize:

    raw = gl.nondet.exec_prompt(prompt)
    cleaned = raw.replace('\x00', '').strip().upper()
    if 'TRUE' in cleaned:
        return 'TRUE'
    return 'FALSE'

### 2. Use `.body.decode()` for web responses

    # Wrong
    page = gl.nondet.web.get(url)

    # Correct
    page = gl.nondet.web.get(url).body.decode('utf-8', errors='replace')[:3000]

### 3. Use `.calldata` not `.value` in validator

    # Wrong
    leader_answer = leaders_res.value

    # Correct
    leader_answer = leaders_res.calldata

### 4. State type annotations required
Class-level annotations are mandatory for persistence:

    class MyContract(gl.Contract):
        my_field: str      # required
        def __init__(self):
            self.my_field = ""  # not enough alone

### 5. No complex generic types
`TreeMap[str, tuple[str, u256]]` causes runtime errors on Bradbury Phase 1.  
Use only: `str`, `bool`, `u256`, `TreeMap` (unparameterized or simple key/value).

## Deploy sequence

    import { createClient } from 'genlayer-js';
    import { testnetBradbury } from 'genlayer-js/chains';
    import { privateKeyToAccount } from 'viem/accounts';
    import { readFileSync } from 'fs';

    const account = privateKeyToAccount('YOUR_PRIVATE_KEY');
    const client = createClient({ chain: testnetBradbury, account });
    const code = readFileSync('./contracts/prediction_market_v2.py', 'utf8');

    const hash = await client.deployContract({
      code,
      args: ['Will ETH exceed 3000 USD?', 'https://coinmarketcap.com/currencies/ethereum/'],
    });
    const receipt = await client.waitForTransactionReceipt({
      hash, 
      status: 'ACCEPTED', 
      retries: 60, 
      interval: 5000
    });
    console.log('Address:', receipt.data.contract_address);

## Serialize BigInt in receipts

    JSON.stringify(receipt, (_, v) => typeof v === 'bigint' ? v.toString() : v, 2)

## Runner ID

    py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6

Reverse-engineered from on-chain data — not in official docs at time of writing.
