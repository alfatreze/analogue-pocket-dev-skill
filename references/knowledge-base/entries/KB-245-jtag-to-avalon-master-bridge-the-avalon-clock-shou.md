---
id: KB-245
title: JTAG-to-Avalon master bridge: the Avalon clock should be at least 2x TCK or System Console accesses time out, a timeout locks the JTAG chain, and single-word access is slow
status: community-reported
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [jtag,system-console,avalon,debug,quartus]
applies_to: Intel Quartus JTAG-to-Avalon master bridge; edition, version and device family not stated; not tested on a Pocket
sources:
  - https://www.intel.com/content/www/us/en/support/programmable/articles/000084688.html
  - https://community.altera.com/discussions/quartus-prime/how-can-i-improve-jtag-to-avalon-master-bridge-write-speeds-through-system-conso/322114
---

## Claim
Intel's troubleshooting advice for System Console memory-access timeouts through the JTAG-to-Avalon master bridge is to run the clock feeding the Avalon-MM interface at least 2x the TCK frequency; a lower TCK (cable setting, for example 16 or 6 MHz instead of a Blaster II's 24 MHz default) is one way to meet the ratio. A System Console timeout during a bridge access can lock the JTAG chain, which makes other users of it, such as SignalTap, unusable until it is cleared. The single-word Tcl calls (master_read_32 / master_write_32) move one item per round trip, roughly 3 ms per access in one community report; master_read_memory / master_write_memory are faster for blocks. One answer says there is no way to speed System Console up.

## Evidence
Seen only through web-search result summaries on 2026-11-11; the primary Intel pages did not load for the fetch tool (301 to a 404 redirector), so they were not read in full. Not Pocket-specific. Confidence stays low until the pages are read or a test is run. Sources: Intel support article 000084688 (last reviewed 2015, per its listing) and an Altera community thread on write speed.

## How to validate on hardware
On a Pocket core with a master bridge and an Avalon clock at least 2x TCK, time 1000 single reads and one 1000-word master_read_memory; then drop the Avalon clock under 2x TCK and confirm the timeout, and check whether jtagconfig still sees the chain afterwards.
