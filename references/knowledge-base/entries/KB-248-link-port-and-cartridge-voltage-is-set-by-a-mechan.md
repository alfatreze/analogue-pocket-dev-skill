---
id: KB-248
title: Link port and cartridge voltage is set by a mechanical switch (5 V when depressed, 3.3 V otherwise), not by core.json; link port power switches on the cartridge rail
status: docs-verified
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [link-port,cartridge,voltage,hardware,uart]
applies_to: Analogue developer docs, external-hardware page (framework 2.x); not tested here
evidence: docs: external-hardware 'Cartridge Bus + Link Port' and core.json link_port (read in full, 2026-11-11)
sources:
  - https://www.analogue.co/developer/docs/external-hardware
  - https://www.analogue.co/developer/docs/core-definition-files/core-json
---

## Claim
Cartridge bus voltage is chosen in hardware by a mechanical switch: 5 V when the switch is depressed (a Game Boy / Game Boy Color style cartridge or adapter does that), 3.3 V when not. Cart power is enabled by core.json (cartridge_adapter). The link port is voltage-controlled and power-switched on the same rail as the cartridge bus. So a core cannot choose the link voltage in core.json: an external serial adapter must be 3.3 V, or sense the link port's VCC, and nothing that depresses the switch should be inserted. Claims that core.json or a 'Game Boy mode' sets 5 V are not what the docs say. All pins go through level translators with fixed direction per pin or group; leave template defaults unless using the port, since a wrong setup with a powered cartridge can corrupt its data.

## Evidence
Docs, external-hardware, section 'Cartridge Bus + Link Port': "Cartridge voltage is determined in hardware by a mechanical voltage selection switch (5v when the switch is depressed, 3.3v when not)"; "Link port power is voltage-controlled and power switched on the same rail as the cartridge bus." core.json docs: link_port is 'Whether link port is utilized'. Source for the contrary wording was an AI-generated search answer pasted by a person, which cites no page for it.

## How to validate on hardware
With a 3.3 V logic probe or scope on the link VCC pin: no cart inserted, then a cart or adapter that depresses the switch; record the voltage in each case and whether core.json changes it. Never connect an adapter's own power output to the link VCC.
