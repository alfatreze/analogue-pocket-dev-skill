# Chip32 VM

Optional loader VM (file named in core.json `chip32_vm`). When present it replaces APF's normal load: it must load the bitstream (`CORE`), load slots (`LOADF` or manual OPEN/READ/COPY), then `HOST 0x4002` to hand back to APF. Runs only on demand (initial boot and when a reloadable slot is picked), not continuously. Hold B to cancel a hung program. Pause Core Boot / Pause Load Data have no effect with Chip32.

Specs: 32-bit, 16 regs (R0-R15), 16-deep 32-bit stack, 8 KB RAM shared with the program (<=2k instructions), instructions 16-bit aligned (odd-length db/text before opcodes misaligns everything: pad with a zero byte). Error vector 0x0000 (first instruction must jump to your error handler); start vector 0x0002. R0 = slot id selected (cold boot: slot index 0's id). R1-R15 are zero on first boot and preserved across resets/reloads (use for state, e.g. "core already loaded" bit); RAM outside the loaded binary is undefined after restart. Return address/jump targets are ANDed with 0x1FFE. Flags Z and C.

Assemble with bass (v19 devel) plus `chip32.vm.arch`: `bass in.asm -o out.bin`. Binaries exist for Win/Linux/macOS (Intel/M1). Reference files: `repo-src/chip32.vm.arch` (full encoding), `repo-src/example_chip32.asm` (complete worked loader). Full opcode docs: `docs-snapshot/chip32-vm__*.txt`.

Instruction groups (see snapshot for precise semantics):
- Load/store: LD (imm/reg/mem, .b/.w/.l), PUSH, POP, PMPW/PMPR (32-bit bridge write/read), PMPBW (byte write: `(Rx&0xF0000000)|((Rx&0x03FFFFFF)<<2)`), 
- ALU: ADD SUB AND OR XOR CMP BIT MUL DIV, shifts ASL LSR ROL ROR.
- Flow: JP/CALL/RET with Z/NZ/C/NC.
- File: OPEN (Rx=slot, Ry<-size, Z=ok), CLOSE, SEEK, READ (<=4 KB into RAM), COPY (file -> bridge address, unlimited size, addresses on 32-bit boundaries), LOADF (load slot with its data.json params; honors ADJ*), ADJFS/ADJFO/ADJLP (override size/offset/load address before LOADF), GETEXT, GETNAME, QUERYSLOT (Z if file present; OPEN on a missing file pops the file browser, so query first).
- Special: CORE (load bitstream id; skipped if already loaded or after JTAG reload), HOST (0x4000 reset, 0x4001 run, 0x4002 continue boot / send Data Slot All Complete), XFILL, RFILL/RSET (SRAM-like random fill), TEST (string compare), ERR, EXIT 0/1, UIVISIBLE (in development), GETTIME (0 unix, 1 BCD date, 2 BCD time), CRC, PRINTF/HEX/DEC (40-char error buffer shown to user, flushed on LF).
- Minimal program: `ld r0,#0; core r0; loadf r?; ld r0,#0x4002; host r0,r0; exit 0` (see example for the reset/run dance on warm reloads).
Debug: Debug Logging + Chip32 Exec Log write every executed instruction to /System/Logs (slow for long loops).
