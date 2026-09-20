# Open questions (unknowns worth a hardware test or a source read)
Add an entry with `scripts/kb.py new` once a question has a claim to test; record the result in the entry.

| # | Question | Why it matters | Cheapest test |
|---|---|---|---|
| OQ-1 | Does Pocket service target 0188 (flush), and with what handshake? No public core implements it. | Persistence design. | Minimal core issuing 0188 for a nonvolatile slot; log result codes and timing; repeat after a successful 0184 write. |
| OQ-2 | Is the size-table entry used by shutdown flush the one at the save slot's data.json POSITION (KB-001), and is it nonzero at Quit? | Save file stays zero. | Read the table back over the bridge before Quit; write a distinctive size; check Saves/. |
| OQ-3 | Does the (size mod 0x10000) delivery truncation (KB-003) still exist on current firmware? | Confounds any slot >= 64 KB. | 0x10200-byte pattern slot, log delivered bytes. |
| OQ-4 | Is 0184 write reliable on current firmware (KB-005)? | Alternative persistence route. | Run the kbmouse-targetdata example unmodified. |
| OQ-5 | Which firmware version is on the test Pocket and which framework version does core.json require? | Behavior differs by version. | Settings > About; record it with every result. |
| OQ-6 | SDRAM: CAS latency, dram_clk phase and refresh vs intermittent return-path faults (KB-021, KB-011). | Persistent SDRAM faults. | Sweep CAS 2/3 and clock phase; correlate with per-seed hold slack. |
| OQ-7 | Exact bridge read timing: cycles between `bridge_rd` and required data. Docs say only 'up to the next read strobe'. | Return-path design. | SignalTap `bridge_rd`, `bridge_addr`, `bridge_rd_data` on back-to-back reads. |
| OQ-8 | What does APF do when the core changes the size-table entry of a nonvolatile slot at runtime? | Growing/shrinking saves. | Resize the entry at runtime, Quit, compare file length. |
| OQ-9 | What lives only in Analogue's Discord (#openfpga-dev) and is not written anywhere public? | Possibly undocumented behaviors. | A person pastes threads; log as community-reported with link/date/author. |
