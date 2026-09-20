# Hardware, buses, video, audio, input

## Buses seen by the core: BRIDGE, PAD, VIDEO, AUDIO
- clk_74a / clk_74b: 74.25 MHz inputs, NOT phase aligned; treat as asynchronous. Bridge is synchronous to clk_74a. Core PLL outputs are separate async groups (see `core_constraints.sdc` set_clock_groups). Synchronise (e.g. 2/3-flop `synch_3`) every crossing between clk_74a and core clocks.
- BRIDGE: framework=controller, core=peripheral; 32-bit address/data, few MB/s, no arbitration, `bridge_endian_little` (template 0 = big-endian words; the template byte-swaps when it is 1). Template decodes `32'hF8xxxxxx` to `core_bridge_cmd` and lets you add e.g. `32'h10xxxxxx`. Write data is broadcast to all devices; read data must be muxed by address. Reads are buffered: data may arrive up to the next read strobe.
- PAD: 1-wire, up to 4 controllers plus heartbeat (loss of heartbeat after JTAG reload makes Pocket reload the core with the same start conditions). Per pad: key[31:0], joy[31:0], trig[15:0].
  key: 0 up,1 down,2 left,3 right,4 A,5 B,6 X,7 Y,8 L1,9 R1,10 L2,11 R2,12 L3,13 R3,14 select,15 start, [31:28] type (0 none,1 Pocket buttons P1 only,2 dock pad no analog,3 dock pad analog,4 keyboard,5 mouse). joy: lx[7:0] ly[15:8] rx[23:16] ry[31:24] unsigned; trig: l[7:0] r[15:8].
  Keyboard is on slot 3: HID scan codes cont3_joy[31:24],[23:16],[15:8],[7:0], cont3_trig[15:8],[7:0]; modifiers cont3_key[15:0]. Mouse on slot 4: buttons cont4_joy[31:16], dx cont4_joy[15:0], report counter cont4_key[15:0], dy cont4_trig[15:0]. Always check the type bits first.

## VIDEO
16x16 to 800x720, 47-~61 Hz, RGB888, pixel clock 1-~50 MHz. Scaler rotates in 90 deg steps and mirrors; pre-scaled Y max 720 (so rotated width <=720).
Signals (all sync to video_rgb_clock; video_rgb_clock_90 is a 90-degree-shifted copy used by APF DDR conversion): video_rgb[23:0], video_de, video_skip, video_vs, video_hs.
Rules: VS one-cycle pulse per frame; HS one-cycle pulse per line, not until 3 cycles after VS; DE asserted once per line for exactly the active pixels; >=1 clock gap between HS and DE and between DE fall and next HS; SKIP only while DE high; RGB must be 0 whenever DE is low except for sideband words.
Frame feature bits (RGB word during VS pulse): [0] rescan previous frame, [1] interlaced, [2] odd field, [3] last field.
End-of-line bits (RGB word after DE falls): [2:0] function 0 = set scaler slot to [23:13] (0-7), effective next frame; last request wins. All-zero default = slot 0.
Template video: 12.288 MHz pixel clock, 320x240@60 (400 clocks/line x 512 lines).

## AUDIO
I2S signed 16-bit stereo, exactly 48 kHz. audio_mclk 12.288 MHz (256 Fs); SCLK 3.072 MHz (64 Fs, re-created in the system FPGA but worth generating for debug); latch on rising SCLK; LRCK low = left; 16 data + 16 spacer bits per channel; first bit delayed one clock after LRCK edge. audio_adc = cartridge audio (pin 31 line level, needs cart power, framework 1.2). Sample-rate adjustment is not allowed.

## RAM and I/O (pin names are in `core_top`)
- PSRAM: 2 chips (`cram0_*`, `cram1_*`), each 2 dies, 16 MB per chip (AS1C8M16PL-70BIN, 1.8 V). Async access or sync burst to 133 MHz. Die select = CE0#/CE1#; never assert both. Hazard: config-register access sequence via last word (3FFFFFh) of each die; special-case that address if the access pattern can match.
- SRAM: 128Kx16 = 256 KB async (AS6C2016-55BIN, 3.3 V), `sram_*`.
- SDRAM: 32Mx16 = 64 MB mobile SDRAM (AS4C32M16MSA-6BIN, 1.8 V), up to 166 MHz, `dram_*` with byte DQM; program mode registers on init; burst for efficiency. Example `io_sdram.v` is a working controller (basicassets example maps 64 MB at bridge address 0 via dataslot loads).
- Cartridge bus (`cart_tran_*`) + link port (`port_tran_*`): level translators; 5 V/3.3 V by mechanical switch; directions per group; keep template defaults unless actively using; pin30 clamped low in 5 V mode until `cart_pin30_pwroff_reset` asserted; wrong translator setup with powered cart can corrupt cartridge data. Cart power per core.json cartridge_adapter.
- IR: tx active-high, PWM only (never DC); rx has AGC, disable (`port_ir_rx_disable`) when unused, allow ms to settle.
- Misc pins: vblank (dock), dbg_tx/rx (UART breakout), user1/user2 solder pads, aux_sda/scl and vpll_feed RFU (leave tied off as template).
- Power/thermal: FPGA fabric 50-300 mW typical; higher-res scaler/display modes raise draw.
