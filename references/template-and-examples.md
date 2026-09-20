# open-fpga repos: what is actually in them (read from source, not docs)

Repos (github.com/open-fpga): core-template (137+ stars), core-example-basicassets, core-example-interact, core-example-basicchip32, core-example-kbmouse-targetdata, bass-chip32 (MIT). Each repo is a Quartus project + dist/ (Pocket folder contents) + output/ (prebuilt .rbf_r).

## Layout
`src/fpga/ap_core.{qpf,qsf}` (Quartus 18.1.1 Lite, Cyclone V), `apf/` (Analogue's framework: apf_top.v, io_bridge_peripheral.v, io_pad_controller.v, mf_datatable.v BRAM for the 0x2000 table, mf_ddio_bidir_12.v, build_id_gen.tcl -> build_id.mif, apf_constraints.sdc, common.v with `synch_3`), `core/` (yours: core_top.v, core_bridge_cmd.v, core_constraints.sdc, PLL mf_pllbase, pin_ddio_clk.v, stp1.stp SignalTap, plus io_sdram.v, mf_linebuf.v in RAM examples). `dist/` = files for the SD card (json, icon.bin, platforms/, assets/). `apf/` should be left alone.

## core_top.v (see `repo-src/core_top.template.v`)
Instantiated by apf_top. Ports: clk_74a/b, cart_tran_* + dirs, port_ir_*, port_tran_* (link), cram0/1_* (PSRAM), dram_* (SDRAM), sram_*, vblank, dbg_tx/rx, user1/2, aux_sda/scl, vpll_feed, video_*, audio_*, bridge_*, cont1-4_key/joy/trig. Template ties unused I/O to safe values (IR rx disabled, translators input, RAMs deselected) and copy that pattern for anything you do not use. `bridge_endian_little = 0` in the template. Status wiring: `status_boot_done = status_setup_done = pll_core_locked_s`, `status_running = reset_n` (so Setup is reached as soon as the PLL locks; a core that needs RAM init must gate `status_setup_done` on it). The `status_setup_done` rising edge triggers the target Ready-to-Run (0140) in the template FSM.

## core_bridge_cmd.v (see `repo-src/core_bridge_cmd.template.v`)
Clocked directly by clk_74a (never a PLL: it reports PLL lock). Host regs in fabric (host_0/4/8, params 0x20+, response 0x40+), data table in BRAM outside. Host parse: 0000, 0010, 0011, 0080, 0082, 008A, 008F, 0090, 00A0, 00A4, 00B0 implemented; everything else returns OK+0xFFFF. `dataslot_requestread/write` `_ack`/`_ok` inputs are tied to 1 in the template (always allow). Target FSM: issues 0140 after setup, then on `target_dataslot_read/write/getfile/openfile` strobes issues 0180/0184/0190/0192 and waits for `bu`/`ok`, exposing `target_dataslot_ack/done/err`. Not present: 0181, 0185, 0188, 0152, host 00B1/00B2/00B8 (added in later framework versions; the examples predate them). Extend the case statement yourself.

## Examples
- basicassets: SDRAM controller (`io_sdram.v`, 64 MB at bridge 0), image + I2S audio loaded from slots by address, user-reloadable slots, menu-state signaling; audio slot id 99 triggers playback on slot write.
- interact: every interact element type writing core registers (addresses 0x00F0000C, 0x00F00010, 0x00100000, 0x00200000 ...), persist true, radio group with mask.
- basicchip32: `src/chip32/example_chip32.asm` reads an 8-byte header from a .dat, picks 4 images, uses OPEN/SEEK/COPY/LOADF, pauses video scanout via a bridge register during reloads, `HOST 0x4000/4001/4002` dance; core.json sets `chip32_vm`.
- kbmouse-targetdata: docked keyboard/mouse, cursor, target read (0180) of images, target write (0184) of framebuffer to slot 0x22 -> `saved.bin` (a deferload slot), `mf_cursorimg/fifo`.
