import { createClient } from 'genlayer-js';
import { testnetBradbury } from 'genlayer-js/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { readFileSync } from 'fs';

const account = privateKeyToAccount('0xf08faba7f33a376ea3aff760cf8243856dfa8c2f5d5dcf31c0f53da3cd1c024e');
const client = createClient({ chain: testnetBradbury, account });
const code = readFileSync('/home/rob/genlayer-prediction-market/contracts/prediction_market_v2.py', 'utf8');

const hash = await client.deployContract({
  code,
  args: ['Will ETH price exceed 3000 USD by June 2026?', 'https://coinmarketcap.com/currencies/ethereum/'],
});
console.log('TX:', hash);
const receipt = await client.waitForTransactionReceipt({ hash, status: 'ACCEPTED', retries: 60, interval: 5000 });
console.log('Address:', receipt.data.contract_address);
