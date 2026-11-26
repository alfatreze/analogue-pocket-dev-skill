---
id: KB-260
title: On a macOS 26.x Command Line Tools install the default SDK failed to link host C test tools until SDKROOT pointed at the versioned MacOSX SDK
status: community-reported
confidence: low
first_seen: 2026-11-26
last_verified: 2026-11-26
tags: [macos,toolchain,host-tools]
applies_to: macOS 26.x with Xcode Command Line Tools only (no full Xcode), Apple silicon; one machine
evidence: first-hand: several host C test builds failed to link and succeeded with the workaround on one machine, 2026-11-24 to 2026-11-25
sources:
  - first-hand: host C test builds on one Mac, 2026-11-24 to 2026-11-25 (no vendor document was read for this claim)
---

## Claim

Host-side C test programs (built with the system compiler for simulation harnesses) failed to link with the default SDK path; the builds worked when `SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk` (the versioned SDK inside the Command Line Tools) was exported. The sessions that hit it attributed the failure to the default SDK's libSystem stub; the exact message was not recorded.

## Evidence

First-hand, one Mac, 2026-11-24 to 2026-11-25: several independent sessions building host harnesses for a core under test reported the link failure and the same fix, and the full host test suite passed with it. Not reproduced on another machine.

## How to validate on hardware

Not a hardware question: build a trivial C program with `cc`, and if linking fails, list `/Library/Developer/CommandLineTools/SDKs/` and retry with `SDKROOT` set to the versioned directory.
