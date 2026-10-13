---
id: KB-166
title: ALM arithmetic modes: dedicated adders and carry chains give cheap adders, but chains start only at certain ALMs and long ones run vertically across LABs
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [alm,arithmetic,carry-chain,adder,timing,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.1: 1.2
---

## Claim
An ALM runs in one of four modes. Normal mode implements two independent functions, or one function of up to six inputs (up to eight data inputs reach the combinational logic). Extended LUT mode implements a 7-input function of the if-else template, leaving the eighth input free for register packing. Arithmetic mode uses two sets of two 4-input LUTs with two dedicated full adders, so each adder can add the outputs of two 4-input functions; using the adder's carry together with a combinational output can save up to 50 percent of the resources. Shared arithmetic mode adds three inputs in one ALM through a dedicated shared-arithmetic chain, which cuts the cost of large adder trees and correlators. Carry chains start in either the first or fifth ALM of a LAB, and a two-bit carry select halves the propagation delay inside the ALM. The compiler links LABs automatically for chains longer than 20 ALMs (10 in arithmetic or shared-arithmetic mode), running them vertically so the connections to memory and DSP columns stay fast, and a chain may span a full column. Chains can use only the top or bottom half of a LAB, leaving the other half for narrower logic. Wide adders therefore consume a long column of ALMs and their delay grows with the chain, which is why a wide add feeding other logic is often a timing-critical path.

## Evidence
Section 1.2.1 to 1.2.4 of the handbook. The closing timing remark is an engineering consequence of the stated chain structure, not a quoted claim.

## How to validate on hardware
Look at a failing path in the timing report: a path through a long carry chain (many carry cells in a row) can be shortened by pipelining the adder into narrower slices or by letting it map to a DSP block (see the DSP entry), and the fit report's ALM count by mode shows how much arithmetic mode the design uses.
