---
id: KB-075
title: Frame-alternating output (interlace fields, per-frame dither) leaves image retention on the Pocket OLED; compare consecutive frames of a still picture
status: community-reported
confidence: medium
first_seen: 2026-09-29
last_verified: 2026-09-29
tags: [video,oled,interlace,testing]
applies_to: Analogue Pocket built-in display (OLED per the source); a BBC Micro community core, 2026-09
sources:
  - https://github.com/plasticbugs/pocket-core-template/blob/HEAD/METHODOLOGY.md
---

## Claim

A core that shows two different images on alternate frames can leave a visible ghost on the Pocket's
panel. The reported case was faithful interlace emulation: each field drew different scanlines from a
different vertical origin at 25 Hz, which a CRT and the eye would merge but a fixed-pixel panel shows as
flicker. In the reported case it was image retention that faded after hours, not permanent burn-in. The
same risk applies to any output that toggles every frame: per-frame dither, a cursor that blinks by
alternating frames, "blend two frames" transparency. The fix is to keep the machine's geometry but draw
the same field every frame, and merge in the core anything the original display left to phosphor
persistence. Comparing against a reference emulator frame by frame never catches this, because it never
compares one frame with the next.

## Evidence

One source: METHODOLOGY.md section 5.23 ("The panel is not a CRT, and burn-in is permanent"), which
quotes a user's report and the fix in a vendored 6845 CRTC. The same section notes that a video.json/RTL
resolution mismatch caused three symptoms at once (squashed picture, missing bottom lines, scaler
flicker); compare KB-014.

## How to validate on hardware

No hardware is needed for the check itself: capture three consecutive frames of a still screen in
simulation or from a frame dump. If neighbouring frames differ while frames two apart are identical, the
output alternates. Stop running the core on a real Pocket until that is fixed.
