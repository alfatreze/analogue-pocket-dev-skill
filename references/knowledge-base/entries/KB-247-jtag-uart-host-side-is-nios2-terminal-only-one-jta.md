---
id: KB-247
title: JTAG UART: host side is nios2-terminal, only one JTAG client at a time, and a program that prints to it can block when no terminal is attached
status: community-reported
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [jtag,jtag-uart,nios,debug,console]
applies_to: Intel Nios II / Platform Designer JTAG UART IP; not tested on a Pocket
sources:
  - https://community.altera.com/discussions/nios-system/jtag-uart-console/109188
  - https://community.altera.com/discussions/nios-system/console-on-jtag-uart--booting-without-terminal/156527
---

## Claim
A JTAG UART core is used from the host with nios2-terminal (select the instance with --instance and the cable with --cable); only one JTAG connection at a time, so a console and a debugger cannot share the link. A program whose console is the JTAG UART can hang when no terminal is attached; the usual workaround is a different console device. Whether nios2-terminal is present in a Quartus Lite install on this host is not established.

## Evidence
Seen only through web-search result summaries on 2026-11-11; the primary Intel pages did not load for the fetch tool (301 to a 404 redirector), so they were not read in full. Not Pocket-specific. Confidence stays low until the pages are read or a test is run. Sources: Altera community threads on JTAG UART console use and on booting without a terminal, plus a FreeBSD manual page for the core.

## How to validate on hardware
Check for nios2-terminal in the Quartus install used for Pocket fits. If present, attach a JTAG UART to a template core's soft CPU, read its output, then run the core without a terminal and confirm it does not block.
