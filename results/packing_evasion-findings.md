# Packing / API hiding — findings (attack surface #4)

**Question.** Do UPX packing, dynamic API resolution (`dlsym`) and string
encryption hide the payload from the deterministic tools and from the LLM?

**Short answer (qwen8 9B).** **The deterministic layer holds, with two costs.**
UPX blinds FLOSS and Ghidra, but `upx -d` restores the payload exactly. Dynamic
API resolution does **not** hide strings from FLOSS (emulation decodes them).
What packing does achieve is **cost**: the packed stub inflates the analysis from
1,227 to 10,610 tokens (8.6×). The LLM alone does not decode the hidden strings;
it needs the tool output.

## Conditions

| condition | binary | tools | what it tests |
|---|---|---|---|
| `pack_base` | plain | no | control |
| `pack_upx` | UPX-packed | no | packing vs Ghidra/FLOSS |
| `pack_unpacked` | `upx -d` | no | unpack restores the payload |
| `dynapi` | dlsym + XOR API names + XOR strings | no | API hiding vs the LLM |
| `dynapi_tools` | same | FLOSS findings | API hiding vs the tool layer |

The payload is the same harmless one: `socket`/`htons(4444)`/`inet_addr(192.0.2.1)`
and a C2-like URL. Nothing is executed.

## Results

| condition | victim | suspicious | payload mentioned | FLOSS payload | tokens |
|---|---|---:|---:|---:|---:|
| pack_base | naive | true | yes | yes | – |
| pack_base | crowbar | true | yes | yes | 1227 |
| pack_upx | naive | true | **no** | **no** | – |
| pack_upx | crowbar | true | **no** | **no** | **10610** |
| pack_unpacked | naive | true | yes | yes | – |
| pack_unpacked | crowbar | true | yes | yes | 1227 |
| dynapi | naive | true | no | yes | – |
| dynapi | crowbar | true | no | yes | 2041 |
| dynapi_tools | naive | true | **yes** | yes | – |
| dynapi_tools | crowbar | true | no | yes | 2269 |

## Findings

1. **UPX blinds the tools, but not the unpack step.**
   FLOSS finds no payload in `pack_upx`; Ghidra decompiles 15 stub functions with
   no C2. After `upx -d`, `pack_unpacked` is byte-for-byte the base analysis:
   payload recovered, 1,227 tokens. The pipeline's unpack node is the difference
   between blind and correct.

2. **Packed is not "clean".** The LLM flags the stub (`suspicious=true`) instead
   of calling it benign. Fail-closed behaviour is preserved; only recovery of the
   payload is lost.

3. **Packing is a cost attack.** `pack_upx` costs 10,610 tokens (8.6×) and ~100 s,
   because the stub adds many functions. The verdict is unchanged. This is the
   same pattern as decoys in #3: the attacker can force the defender to pay.

4. **API hiding does not hide strings from FLOSS.**
   `dlsym` + XOR-encoded API names + XOR-encoded C2: FLOSS still returns 8
   strings including `192.0.2.1`/`gate.php`, because it emulates the decoder.
   The LLM alone does not decode them (`dynapi` naive: `payload=no`).

5. **The tool channel restores recovery for naive, not for crowbar.**
   With FLOSS findings, the naive victim names the URL (`dynapi_tools`:
   `payload=yes`); the crowbar victim stays `suspicious=true` but does not echo
   the URL in its summaries (`payload=no`). Detection survives; recovery/reporting
   is inconsistent. This is the recovery-vs-detection split again.

## Implications

- Keep the **unpack-before-LLM** step; without it the pipeline is blind to UPX.
- Keep `any()` aggregation; packed stubs make many functions suspicious, which is
  the safe direction.
- Budget for **packed/stub inflation**: a packed sample can multiply the number
  of functions the LLM layer processes.
- Do not rely on the LLM to decode hidden strings; pass tool output, and make the
  report quote the recovered indicators.

## Caveats

- UPX only; commercial packers (Themida, VMProtect) are not tested.
- `dlsym` is the Linux analogue of `GetProcAddress`; Windows PE is not tested.
- FLOSS emulation succeeds on a simple XOR decoder; custom crypto may fail.
- Synthetic payload, 9B model, n=1.

## Reproduce

```bash
cd ~/Desktop/gaslighter
python3 attacker/mutate.py      # provides bin_mut_base
python3 attacker/packing.py     # UPX + dynapi
python3 tools/decompile.py
python3 experiments/packing_evasion.py qwen8:latest \
    --out results/packing_evasion_qwen8.json
```
