---
id: KB-241
title: Target command 0152 (Debug Event Log) lets a core write a time-stamped 32-bit value to the APF debug log at runtime, a trace channel in the shipping build
status: docs-verified
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [debug,trace,target-commands,logging]
applies_to: framework 1.2 and later; per the Analogue developer docs
evidence: docs: host-target-commands 0x0152 and changelog 1.2 (read in full 2026-11-11)
sources:
  - https://www.analogue.co/developer/docs/host-target-commands
  - https://www.analogue.co/developer/docs/changelog/1-2
---

## Claim
Target command 0x0152 (Debug Event Log) takes one parameter, a custom 32-bit event id, and prints it to the debug log with a timestamp while the core runs. It is a trace channel that needs no extra hardware and works in the shipping bitstream. The log is the one written under /System/Logs/ when Debug Logging is enabled (see KB-242). The shipped template's command FSM never issues it (KB-007), so a core must add the command itself. Throughput, how many events survive a burst, and whether the Developer menu is reachable on every unit are not documented.

## Evidence
Docs, host-target-commands page, Target Command List: "0x0152 Debug Event Log. Parameters: 1 [31:0] Custom event ID to print in Debug Log. Response: 0". Docs, changelog 1.2: "A new Target command [0152 Debug event log] will let cores write a time-stamped 32-bit number to the debug log during runtime." The template gap is from KB-007 (source read).

## How to validate on hardware
Add a core-side event sender (a FIFO feeding the target command channel). Send a counter value every N ms and a burst of 1000 events; read /System/Logs/ after quitting the core. Record the timestamp resolution, the maximum sustained rate, and any lost or reordered events. Check on a consumer unit whether Debug Logging can be enabled.
