---
id: KB-059
title: A linker script's DEFINED() inside a MEMORY block's LENGTH silently has no effect in riscv-none-elf-ld
status: community-reported
confidence: medium
first_seen: 2026-09-25
last_verified: 2026-09-25
tags: [toolchain,linker,riscv,gnu-ld]
applies_to: riscv-none-elf-ld from xpack-riscv-none-elf-gcc-15.2.0-1 (rv32im/ilp32 bare-metal target)
sources:
  - a Cyclone V openFPGA core project (repository name withheld per this skill's own no-project-naming convention)
---

## Claim

Making a `MEMORY` block's region `LENGTH` conditional via `LENGTH = DEFINED(SYM) ? A : B`, where `SYM` is
meant to be supplied via `-Wl,--defsym=SYM=1` on the link command line, silently has NO effect in this
toolchain: the link succeeds with no error or warning, but the region always resolves to the same size
regardless of whether the `--defsym` flag is passed. This is a genuinely dangerous failure mode because
nothing in the build's own output signals it -- a build "succeeds" while silently ignoring the intended
configuration, and the only way to catch it is to check the actual derived symbol values (e.g. `_stack_top`)
with `nm` on the resulting ELF and compare across both settings.

`DEFINED()` used in an ordinary symbol assignment ELSEWHERE in the same script (not inside a `MEMORY`
block's `ORIGIN`/`LENGTH` expression) works exactly as expected: `_limit = DEFINED(SYM) ? A : B;
_stack_top = _limit;` correctly produces two different linked images, confirmed via `nm`.

## Evidence

Reproduced concretely: `MEMORY { ram : ORIGIN = 0x0, LENGTH = DEFINED(RAM_192K) ? 0x30000 : 0x40000 } ...`
was built twice, once with `-Wl,--defsym=RAM_192K=1` and once without. Checking `_stack_top`'s value with
`riscv-none-elf-nm` after each link showed IDENTICAL results (`0x00040000`, the "else" branch) in both
cases -- the flag had no effect whatsoever, and the link itself reported no error, no warning, nothing to
indicate the conditional had been silently ignored. Moving the identical conditional logic out of the
`MEMORY` block into a plain symbol assignment placed later in the script (`_ram_limit =
DEFINED(RAM_192K) ? (ORIGIN(ram)+0x30000) : (ORIGIN(ram)+LENGTH(ram)); _stack_top = _ram_limit;`, with
`MEMORY`'s own `LENGTH` left as a fixed, unconditional literal) fixed it immediately: the SAME `nm` check
now showed genuinely different `_stack_top` values (`0x30000` vs `0x40000`) depending on whether the
`--defsym` flag was passed, exactly as intended.

## How to validate on hardware

Not a hardware question -- a pure toolchain/linker-script behavior, confirmed via `nm` inspection of the
linked ELF, not simulation or silicon. To reproduce on a different toolchain version or a different `ld`
(BFD vs. LLD, or a different GNU binutils release): declare a `MEMORY` region with a `DEFINED()`-conditional
`LENGTH`, link with and without the corresponding `--defsym`, and check whether a symbol derived from
`LENGTH(region)` (e.g. `ORIGIN(region) + LENGTH(region)`) actually changes between the two builds via `nm`.
If it does change on some other `ld` version, this entry should be narrowed to name the specific broken
version(s) rather than the whole `ld` family; not yet checked against any `ld` besides the one named above.
