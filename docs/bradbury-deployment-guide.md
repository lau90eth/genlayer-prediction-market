# How to Actually Deploy on GenLayer Bradbury Testnet

This guide documents everything you need to successfully deploy and interact with
Intelligent Contracts on GenLayer Bradbury Testnet (Phase 1).
Most of this was learned by trial and error — none of it is in the official docs.

---

## 1. Environment Setup

### Requirements
- Node.js 20+ (via nvm recommended)
- GenLayer CLI v0.39.0+
- WSL2 Ubuntu (if on Windows)

### Install
    # Install nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    source ~/.bashrc

    # Install Node 20
    nvm install 20
    nvm use 20

    # Install GenLayer CLI
    npm install -g genlayer

    # Verify
    genlayer --version

### Configure for Bradbury
    genlayer config set network testnet-bradbury
    genlayer account import # import your private key

---

## 2. Critical: File Encoding (Windows/WSL)

**This is the #1 cause of deployment failures on Windows.**

If you create `.py` files using PowerShell (`Set-Content`, `echo`, etc.),
they will have UTF-8 BOM + CRLF line endings. GenVM wraps contract code
in JSON at startup — BOM breaks JSON parsing with:
"msg": "invalid_contract" / "expected value at line 1 column 2"

### Fix: Always create files in WSL
    # CORRECT — creates LF, no BOM
    cat > contract.py << 'PYEOF'
    # your contract code here
    PYEOF

    # Verify encoding
    file contract.py          # must show: ASCII text
    hexdump -C contract.py | head -1   # must start with: 23 20 (not EF BB BF)

Never use PowerShell `Set-Content` or Windows Notepad to create contract files.

---

## 3. Runner ID

**The runner ID in the official docs is wrong for Bradbury.**

The format comment `# v0.1.0` is obsolete. GenVM expects a JSON manifest
on the first line. The runner IDs `py-genlayer:test` and `python:latest`
are invalid on non-debug testnets.

### Correct runner for Bradbury (Phase 1)
    # { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

This was reverse-engineered from successful transactions on the Bradbury explorer.
Check `https://explorer-bradbury.genlayer.com` for the latest working runner
by inspecting recent successful `CONTRACT_DEPLOYMENT` transactions.

---

## 4. Contract Structure

### Minimal working contract
    # { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
    from genlayer import *

    class MyContract(gl.Contract):
        # REQUIRED: class-level type annotations for ALL persistent fields
        my_value: str

        def __init__(self):
            self.my_value = ""

        @gl.public.write
        def set_value(self, value: str) -> None:
            self.my_value = value

        @gl.public.view
        def get_value(self) -> str:
            return self.my_value

### Critical rules

**1. Class-level type annotations are mandatory for storage persistence.**
    # WRONG — state is NOT persisted after execution
    class MyContract(gl.Contract):
        def __init__(self):
            self.value = ""        # this disappears after each call

    # CORRECT — state IS persisted
    class MyContract(gl.Contract):
        value: str                 # class-level annotation required
        def __init__(self):
            self.value = ""

**2. Supported storage types**

| Type              | Example              |
|-------------------|----------------------|
| `str`             | `name: str`          |
| `bool`            | `active: bool`       |
| `u256`            | `count: u256`        |
| `i32`, `u32`, ... | `amount: u32`        |
| `Address`         | `owner: Address`     |

Do NOT use `int` — use `u256` or sized integers instead.

---

## 5. LLM / Non-deterministic Pattern

**`gl.nondet.exec_prompt` cannot be called directly in a `@gl.public.write` method.**
It must be wrapped in `gl.vm.run_nondet_unsafe` with explicit `leader_fn`
and `validator_fn`.

    # WRONG — causes exit_code 1 on all validators
    @gl.public.write
    def ask(self, question: str) -> None:
        result = gl.nondet.exec_prompt("Answer: " + question) # crashes
        self.answer = result

    # CORRECT
    @gl.public.write
    def ask(self, question: str) -> None:
        q = question                     # copy to local variable before nondet context
        prompt = "Answer in one sentence: " + q

        def leader_fn() -> str:
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        self.answer = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

**Important:** Never access `self.*` storage fields inside `leader_fn` or
`validator_fn`. Copy all needed values to local variables before the nondet block.

    # WRONG
    def leader_fn() -> str:
        return gl.nondet.exec_prompt("Question: " + self.question) # crashes

    # CORRECT
    q = str(self.question)      # copy first
    def leader_fn() -> str:
        return gl.nondet.exec_prompt("Question: " + q)

---

## 6. Deploying Contracts

### Without constructor arguments
    genlayer deploy --contract my_contract.py

### With constructor arguments
    # CORRECT
    genlayer deploy --contract my_contract.py --args '"My argument"'

    # WRONG
    genlayer deploy --contract my_contract.py --args '["My argument"]'

The CLI wraps args in a list internally — passing `["arg"]` results in
a list-of-list being passed to the constructor.

### Getting the contract address
The CLI sometimes times out before printing the address. If this happens:

    # Option 1
    genlayer deploy --contract my_contract.py 2>&1 | grep -i "contract address"

    # Option 2: via genlayer-js
    node -e '
    import("genlayer-js").then(async ({createClient}) => {
      const {testnetBradbury} = await import("genlayer-js/chains");
      const client = createClient({ chain: testnetBradbury });
      const receipt = await client.waitForTransactionReceipt({
        hash: "0xYOUR_TX_HASH",
        status: "ACCEPTED",
        retries: 3,
        interval: 1000,
      });
      console.log(JSON.stringify(receipt, (k,v) => typeof v==="bigint"?v.toString():v, 2));
    });
    '

---

## 7. Reading and Writing

### Read (view) calls
    genlayer call <contract_address> <method_name>
    genlayer call 0xABC...123 get_value

### Write transactions via CLI
    genlayer write <contract_address> <method_name> [args]
    genlayer write 0xABC...123 set_value "hello"

**Note:** CLI write transactions may fail with `execution reverted` on Bradbury.
Use genlayer-js instead.

### Write transactions via genlayer-js (recommended)
    # write.mjs
    import { createClient } from 'genlayer-js';
    import { testnetBradbury } from 'genlayer-js/chains';
    import { privateKeyToAccount } from 'viem/accounts';

    const account = privateKeyToAccount('0xYOUR_PRIVATE_KEY');
    const client = createClient({ chain: testnetBradbury, account });

    const txHash = await client.writeContract({
      address: '0xYOUR_CONTRACT_ADDRESS',
      functionName: 'set_value',
      args: ['hello'],
    });

    console.log('TX:', txHash);
    console.log('Explorer: https://explorer-bradbury.genlayer.com/tx/' + txHash);

    # Run
    npm install genlayer-js
    node write.mjs

---

## 8. Transaction Lifecycle
Transactions on Bradbury go through 7 steps:

1. Transaction Submitted
2. Activation
3. Leader proposal
4. Vote commit
5. Leader reveal
6. Vote reveal → **AGREE** or **DISAGREE**
7. Decided: Accepted / Accepted (Error)

**Typical timing:** 5-10 minutes from submission to ACCEPTED.

`ACCEPTED (ERROR)` means all validators agreed on an error — check explorer details.

---

## 9. Common Errors

| Error                                      | Cause                                    | Fix |
|--------------------------------------------|------------------------------------------|-----|
| `invalid_contract` / BOM                   | UTF-8 BOM + CRLF                         | Use `cat > file.py <<'EOF'` in WSL |
| `invalid runner id`                        | Wrong runner ID                          | Use pinned runner from section 3 |
| `AttributeError: object has no attribute`  | Missing class-level annotation           | Add `field: type` at class level |
| `AttributeError: 'list' object has no...`  | Wrong `--args` format                    | Use `'"string"'` |
| `execution reverted`                       | Consensus contract mismatch              | Use genlayer-js with `testnetBradbury` |
| `exit_code 1` on validators                | `exec_prompt` called directly            | Wrap in `gl.vm.run_nondet_unsafe` |

---

## 10. Explorer
Bradbury explorer: `https://explorer-bradbury.genlayer.com`

## Related Tools

[genvm-recon](https://github.com/lau90eth/genvm-recon) — Static analyzer that detects the issues documented in this guide before deployment.

---

*Guide by [lau90eth](https://github.com/lau90eth) — May 2026*
*Based on hands-on experience deploying 4 contracts on Bradbury Phase 1*

