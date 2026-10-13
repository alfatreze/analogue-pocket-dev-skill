---
id: KB-157
title: JTAG configuration takes precedence over every other Cyclone V configuration scheme, and compressed bitstreams do not work over JTAG
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [configuration,jtag,sof,rbf,compression,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.7: 7.1 (Table 92), 7.10, 7.11
---

## Claim
JTAG instructions override whichever scheme the MSEL pins select, so a JTAG download replaces a configuration that was loaded by another path. Quartus produces an SRAM Object File (.sof) for JTAG; a .rbf or Jam/STAPL file can be used with other tools. JTAG runs at up to 33 MHz and is the one scheme that supports neither decompression, design security nor remote system update. Compression (typically a 30 to 55 percent smaller file) works in every other scheme and is enabled before compilation in Device and Pin Options or afterwards in Convert Programming Files; in an FPP chain, compressed and uncompressed data cannot be mixed because the DCLK-to-data ratio differs. Fast Passive Parallel (8 or 16 bits, up to 125 MHz) is the fastest scheme and needs two DCLK falling edges after CONF_DONE goes high to start initialisation.

## Evidence
Table 92 and sections 7.10, 7.11 and 7.6 of the handbook. The precedence statement is explicit in 7.10.

## How to validate on hardware
To confirm precedence on a board, load a .sof by JTAG and observe that the previously loaded design stops running; loading the design again by the board's normal path replaces the JTAG image, since both write the same volatile configuration RAM.
