---
id: KB-007
title: Template core_bridge_cmd never issues 0188 flush, 0181, 0185 or 0152
status: source-verified
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [template, target-commands, flush]
applies_to: open-fpga template and examples as of 2026-09-20
sources:
  - https://github.com/open-fpga/core-template/blob/main/src/fpga/core/core_bridge_cmd.v
  - https://github.com/open-fpga/core-example-kbmouse-targetdata/blob/main/src/fpga/core/core_bridge_cmd.v
  - https://github.com/janisc/openfpga-NGPC/blob/main/target/pocket/core_bridge_cmd.v
---

## Claim
The stock target FSM implements only 0140, 0180, 0184, 0190, 0192. Flush (0188), 48-bit read/write (0181/0185) and debug log (0152) are documented but absent from the official template, the four examples and the NGPC copy of the module. No community source found shows a working 0188 implementation.

## Evidence
Read of each core_bridge_cmd.v. Gateman's generated docs list a TARG_ST_SLOTFLUSH state, but no implementing source was found in that repo.


## How to validate on hardware
Implement 0188 in a copy of the FSM, issue it for a known slot, and record the result code and timing. Because normal shutdown flush is APF-driven (see KB-001), 0188 may not be needed for persistence at all.
