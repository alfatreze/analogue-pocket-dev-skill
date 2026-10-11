---
id: KB-126
title: A stereo (TRS) plug in a balanced audio-interface input records LEFT MINUS RIGHT: identical channels cancel and the response and distortion you measure are those of the difference
status: hardware-validated
confidence: medium
first_seen: 2026-10-08
last_verified: 2026-10-08
tags: [audio,measurement,capture,loopback]
evidence: Recorded on an Analogue Pocket into a Volt 1 combo input: a tone with the right channel inverted read 11.6 dB louder and 42 dB cleaner than the normal tone at the same gain.
applies_to: any audio capture of a stereo headphone/line output through a balanced (TRS) interface input
sources:
  - developer hardware measurement, 2026-10-08 (project-internal)
---

## Claim
A 3.5 mm stereo plug through a 6.35 mm TRS adapter into a balanced (TRS) interface input is captured as tip minus ring: left minus right. When the two channels carry the same signal they cancel to the small mismatch of the two output stages, which grows with frequency (a rising apparent response, early clipping at 10-12 kHz, distortion numbers that describe the difference signal, a noise floor and spurs that are not those of one channel). Use a mono (TS) plug or adapter, tip only, to measure one channel.

## Evidence
Analogue Pocket headphone jack into a Volt 1 combo input: a -6 dBFS 1 kHz tone with the right channel inverted recorded 11.6 dB louder and 42 dB cleaner (THD -85.5 against -43.4 dB) than the normal tone at the same gain; the 10 kHz tone read at least 7 dB and a 12 kHz section 13 dB above the 1 kHz gain. The ch0 and ch1 of the stereo WAV were identical (the interface is mono).

## How to validate on hardware
Play a tone file with one channel inverted next to the normal file at the same gain: a differential input reads the inverted one much louder. Then repeat the key measurements through a TS plug.

