---
id: KB-237
title: Handheld display path is RGB565; docked output is higher depth (user-supplied claim, matches a measurement)
status: community-reported
confidence: low
first_seen: 2026-11-08
last_verified: 2026-11-08
tags: [video,color-depth,screenshots]
applies_to: Analogue Pocket, openFPGA core driving 24-bit RGB888 at 800x720, Pocket firmware as of 2026-11; handheld mode
sources:
  - https://www.reddit.com/r/AnaloguePocket/comments/18vdn2z/color_accuracy_bad_only_16bit/
  - https://www.analogue.co/pocket
---

## Claim

In handheld mode the Pocket's internal hardware processes and shows RGB565 (16-bit, 65,536 colours) on its 1600x1440 screen, whatever depth the core sends; docked, the output steps up to about 21-bit colour for external displays. (Pasted by the project owner from a web summary quoting Wikipedia, analogue.co, an openFPGA-GBA README and a Reddit thread; I did not open those pages, so the wording and the 21-bit figure are unverified.)

## Evidence

Hardware, 2026-11-09 (a test core, build 2): a core sending exact RGB888 at 800x720 (a ramp whose levels are 1 apart every 3 pixels, plus a gradient and a texture) came back in Pocket screenshots with exactly 5 bits in R and B (0, 8, 16, 24, 33, 41 ... bit replication) and 6 bits in G (0, 4, 8, 12 ...), in all four patterns. The core's video path has no 565 stage (checked in the RTL; the same path is pixel-exact in simulation), so the reduction is on the Pocket side in handheld mode. A read-back of the whole plane through the core's SDRAM mailbox (432,000 words) was then exact, 0 bad, so the reduction is not in the core's memory. Not yet measured: what a docked screenshot or output shows.

## How to validate on hardware

(1) Run the plane read-back check of the next test build: an exact read-back of the plane proves the reduction is after the core's memory. (2) Repeat the ramp docked and read the HDMI output or a screenshot: more than 32/64/32 distinct levels means the dock keeps more depth. (3) Dither test: send the same ramp with a 4x4 ordered dither to 565 in the core; if the Pocket truncates, the dithered picture shows no banding in handheld.
