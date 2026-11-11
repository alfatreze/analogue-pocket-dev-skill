---
id: KB-239
title: 800x720 scaler slot switch via the end-of-line sideband word works on hardware, 33 ms
status: community-reported
confidence: medium
first_seen: 2026-11-09
last_verified: 2026-11-09
tags: [video,scaler,video-json]
applies_to: Analogue Pocket, openFPGA core, video.json with two scaler_modes (400x360 and 800x720, both 10:9), 40 MHz pixel clock, Pocket firmware as of 2026-11, handheld
sources:
  - hardware test 2026-11-09
---

## Claim

One core can switch between a 400x360 and an 800x720 picture at run time with two scaler modes in video.json: the scaler slot is chosen by the RGB word the core drives in the cycle right after DE falls on every line (the word is {10'b0, slot, 13'b0}, slot in bits 23:13, function bits 2:0 = 0), and the change takes effect on the next frame. An 800x720 picture can be generated at a 40 MHz pixel clock with a 900 x 740 total (60.06 Hz): active window starting at horizontal count 16 and line 8, horizontal sync at 840 to 879, vertical sync at lines 734 to 737.

## Evidence

Hardware, 2026-11-09, handheld: 800x720 test patterns showed with exact geometry (a one-pixel white frame on the outermost pixels at x 0 and 799, lines 0 and 719, nothing cropped or shifted); 20 round trips between the two modes, 40 of 40 completed, worst time from the request to the new mode on the bus 33 ms (two frames of the pending/switch sequence), the mode was usable in both directions. The 400x360 side used a 1,666-clock line with 400 data-enable clocks. The video timing positions are those of another project's 800x720 mode that had run on a Pocket. Not tested: the dock.

## How to validate on hardware

Declare two scaler_modes (slot 0 400x360, slot 1 800x720), drive the slot word on every line for a frame before switching the scan-out geometry, request a switch every 150 ms 20 times, count completed switches in the core and take a screenshot in each mode.
