---
id: KB-246
title: Virtual JTAG (sld_virtual_jtag): TCK clocks the whole SLD infrastructure (10 MHz max with an Intel cable), so cross to the user clock; quartus_stp drives it with lock, virtual IR shift, virtual DR shift
status: community-reported
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [jtag,virtual-jtag,quartus-stp,cdc,debug]
applies_to: Intel Quartus Virtual JTAG IP (sld_virtual_jtag), 20.3 user guide; not tested on a Pocket
sources:
  - https://www.intel.com/content/www/us/en/docs/programmable/683705/20-3/design-flow-of-the-virtual-jtag-core.html
  - https://intel.com/content/www/us/en/docs/programmable/683432/21-4/tcl_pkg_jtag_ver_1.0_cmd_device_virtual_dr_shift.html
---

## Claim
Virtual JTAG's TCK clocks the whole SLD infrastructure (10 MHz maximum when an Intel programming cable is used, per the guide), so signals between the JTAG clock domain and the application clock need ordinary clock-domain-crossing practice. From the host, quartus_stp Tcl drives an instance: lock the device, shift the virtual IR (device_virtual_ir_shift) to select the instruction, then the DR (device_virtual_dr_shift; hex or binary value strings, not numbers), then unlock. A virtual IR shift is needed before DR shifts to activate the instance; -show_equivalent_device_ir_dr_shift shows the underlying shifts when an instance is not found. Intel recommends a bypass register as the active register for unmapped IR values. In the timing analyzer, altera_reserved_tck is a hidden signal; declare the JTAG clock asynchronous to the user clock.

## Evidence
Seen only through web-search result summaries on 2026-11-11; the primary Intel pages did not load for the fetch tool (301 to a 404 redirector), so they were not read in full. Not Pocket-specific. Confidence stays low until the pages are read or a test is run. Sources: Intel Virtual JTAG user guide 683705 (20.3) and the Quartus scripting reference for device_virtual_dr_shift.

## How to validate on hardware
Instantiate sld_virtual_jtag in a Pocket core with a loopback register window; run the Tcl lock, IR, DR sequence with quartus_stp and compare captured data with the expected bit order; confirm the instance is found after a JTAG reload of the bitstream.
