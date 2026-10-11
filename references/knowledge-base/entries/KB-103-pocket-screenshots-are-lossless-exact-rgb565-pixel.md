---
id: KB-103
title: Pocket screenshots are lossless exact RGB565 pixels: a 16-bit-per-pixel data channel off the core
status: hardware-validated
confidence: medium
first_seen: 2026-10-04
last_verified: 2026-10-04
tags: [video,screenshots,data-channel]
applies_to: Analogue Pocket, openFPGA core outputting 400x360 RGB565 video, Pocket firmware as of 2026-10; screenshot via the Pocket's own screenshot combination (saved to Memories/Screenshots)
evidence: Hardware: four known test patterns drawn by the core came back 100.000% pixel exact from Pocket screenshots; 13 real screenshots show exactly 32/64/32 distinct levels in R/G/B; a real binary record read back byte for byte.
sources:
  - developer hardware measurement, 2026-10-04 (project-internal)
---

## Claim
A Pocket screenshot of a core's screen is a lossless PNG of the exact pixels the core displayed, with no scaling, filtering or dithering. A core that drives RGB565 (expanded to 8 bits per channel by bit replication on output) therefore has a 16-bit-per-pixel data channel to the host: a 400x360 screen carries up to 288,000 bytes. The file is named `YYYYMMDD_HHMMSS.png` after the Pocket's clock, so the capture time is free metadata. A QR code is unnecessary on this path; the pixels can carry a binary record directly.

## Evidence
Developer measurement, 2026-10-04. (1) 13 real screenshots from earlier sessions: 400x360, 8-bit RGB, exactly 32/64/32 distinct levels in R/G/B, all equal to the RGB565 bit-replication values. (2) Four known test patterns drawn by the core (dense pseudo-random 16-bit field, 1 px checkerboard, smooth gradient, counter) came back 100.000% pixel exact, 0 wrong pixels, compared after converting back to RGB565 (host script). (3) A real diagnostics record (231, 421 and 883 bytes) written into the pixels in three layouts decoded byte for byte, identical to the same record read from a QR code on the same screen. Lossy copies are NOT preserved: JPEG, resizing and camera photos corrupt dense modes; a 4x4-pixel, 2-bit-per-channel mode survived JPEG q80+ and box/Lanczos/nearest/bicubic resizing on the host but not a heavy bilinear 50% downscale (about 14% of cells wrong).

## How to validate on hardware
Draw a known pattern (random 16-bit values, 1 px checkerboard), take a Pocket screenshot, convert the PNG to RGB565 (r>>3, g>>2, b>>3) and compare every pixel with the generator. 100% exact means the channel is lossless for that content.
