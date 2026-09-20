---
id: KB-001
title: Nonvolatile slot flush size comes from the core's data-slot size table, indexed by slot position
status: source-verified
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [save, size-table, nonvolatile, flush]
applies_to: framework 1.1-2.3 as observed in shipping cores
sources:
  - https://www.analogue.co/developer/docs/core-definition-files/data-json
  - https://github.com/agg23/openfpga-NES/blob/main/target/pocket/core_top.v
  - https://github.com/janisc/openfpga-NGPC/blob/main/target/pocket/core_top.v
---

## Claim
At shutdown APF writes a nonvolatile slot back to SD using the size held in the core's Dataslot ID/Size Table (BRAM behind bridge 0xF8002000, fed by `datatable_addr/wren/data` into `core_bridge_cmd`). If the entry is 0 (no file was loaded), the flush writes 0 bytes: no file and no error. The entry is addressed by the slot's POSITION in data.json, not its id: word `[position*2]` = id, `[position*2+1]` = size.

## Evidence
data.json docs: 'size of the file is determined by the Dataslot ID/Size Table BRAM in the core'. agg23 NES core_top drives `datatable_addr <= 1*2+1; datatable_data <= has_save ? 32'h40000 : 0;` continuously, with the comment 'Data slot index 1, not id 1'. NGPC core_top explains that with no file at boot the entry held zero, 'so every flush wrote zero bytes: no file, no error, forever', and fixed it by writing the size itself to address 7 (slot index 3). LiteX docs add that writing its `file_size` register updates the internal size representation of a slot (and can corrupt reads of read-only slots).


## How to validate on hardware
Write a distinctive size (e.g. 0x2000) into the table entry for the save slot's POSITION (index*2+1) from clk_74a while the core runs, run for a while, Quit the core from the menu, and check whether Saves/... appears with that length. Then repeat with the entry left at 0 to confirm the zero-byte behavior. Read the table back over the bridge (0xF8002000 + index*8 + 4) to confirm the write landed.
