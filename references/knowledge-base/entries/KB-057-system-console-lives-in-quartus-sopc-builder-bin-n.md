---
id: KB-057
title: system-console lives in quartus/sopc_builder/bin, not quartus/bin; ISSP Tcl service type is issp not source_probe
status: community-reported
confidence: low
first_seen: 2026-09-24
last_verified: 2026-09-24
tags: [quartus,jtag,issp,system-console,toolchain]
applies_to: unknown
evidence: Reverted from source-verified: validator requires >=2 independent sources for that tier and this entry only has one (the direct tool run, no second citable source). Confirmed directly against a live system-console --cli session regardless -- see the Evidence section for the exact commands run and outputs observed.
sources:
  - https://www.intel.com/content/www/us/en/docs/programmable/683705
---

## Claim

In a Quartus Prime Lite/Standard 25.1std install, `system-console` is not in the main
`<quartus>/bin` directory alongside `quartus_pgm`/`quartus_stp`/`jtagconfig` -- it lives at
`<quartus>/sopc_builder/bin/system-console`. Once launched, the Tcl service type for In-System
Sources and Probes (ISSP) is `issp`, not `source_probe` (a natural guess from the megafunction's
own name, `altsource_probe` -- `get_service_paths source_probe` errors with "The service type
source_probe is not valid"). The real commands, confirmed present via `info commands *issp*`:
`issp_read_probe_data <service-path>`, `issp_write_source_data <service-path>`,
`issp_get_instance_info <service-path>`, used with the generic `open_service issp <path>` /
`close_service issp <claimed>` pair (both of which exist as real Tcl procs, confirmed by
triggering their argument-count error messages).

## Evidence

Confirmed directly against a live `system-console --cli` session on Quartus Prime Lite/Standard
25.1std.0 Build 1129 (Cyclone V target project), 2026-09-24: `find` located the binary at
`quartus/sopc_builder/bin/system-console` after it was absent from `quartus/bin`; `get_service_types`
returned `bytestream dashboard design device io_bus issp jtag_debug loopback marker master monitor
packet plugin processor slave sld trace trace_db` (no `source_probe` in the list); `info commands
*issp*` returned exactly the four commands above; calling each with no/wrong arguments produced a
real "Missing argument <service-path>" / "Path badpath cannot be found" error, confirming they exist
and take the arguments described. No JTAG cable was connected during this check -- `get_service_paths
issp` returned empty, as expected with no hardware attached -- so this confirms the TOOL/COMMAND
SYNTAX only, not an actual live ISSP read over real JTAG hardware.

## How to validate on hardware

With a JTAG cable connected to a running core that has an ISSP instance: `set p [lindex
[get_service_paths issp] 0]`, `set c [open_service issp $p]`, `issp_read_probe_data $c`, `close_service
issp $c`. Record the exact return format of `issp_read_probe_data` (binary string? hex? Tcl list?) --
not yet observed with real data.
