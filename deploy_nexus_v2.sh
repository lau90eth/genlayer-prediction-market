#!/bin/bash
PRIVKEY="0xf08faba7f33a376ea3aff760cf8243856dfa8c2f5d5dcf31c0f53da3cd1c024e"
BASE="/home/rob/genlayer-prediction-market"

for CONTRACT in prediction_market parametric_insurance dispute_resolver hello_ai; do

cat > /tmp/deploy_${CONTRACT}_v2.mjs << JSEOF
import { createClient } from 'genlayer-js';
import { testnetBradbury } from 'genlayer-js/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { readFileSync } from 'fs';

const account = privateKeyToAccount('${PRIVKEY}');
const client = createClient({ chain: testnetBradbury, account });
const code = readFileSync('${BASE}/contracts/${CONTRACT}_v2.py', 'utf8');

const args = '${CONTRACT}' === 'prediction_market'
  ? ['Will ETH price exceed 3000 USD by June 2026?', 'https://coinmarketcap.com/currencies/ethereum/']
  : '${CONTRACT}' === 'parametric_insurance'
  ? ['AZ100']
  : [];

const hash = await client.deployContract({ code, args });
console.log('${CONTRACT} TX:', hash);

const receipt = await client.waitForTransactionReceipt({
  hash,
  status: 'ACCEPTED',
  retries: 60,
  interval: 5000,
});
console.log('${CONTRACT} address:', receipt.data.contract_address);
JSEOF

echo "Deploying ${CONTRACT}_v2..."
node /tmp/deploy_${CONTRACT}_v2.mjs

done
