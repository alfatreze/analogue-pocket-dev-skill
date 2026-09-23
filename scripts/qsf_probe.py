#!/usr/bin/env python3
"""Test whether a Quartus feature/assignment is accepted and takes effect in YOUR edition (e.g. Lite 25.1, Cyclone V).

Use this instead of trusting a web claim that an option is "Standard/Pro only".

  qsf_probe.py make DIR --assign 'set_global_assignment -name PHYSICAL_SYNTHESIS_EFFORT EXTRA' [--assign ...]
      writes a tiny Cyclone V (5CEBA4F23C8) project into DIR: a 32-bit adder chain plus a 512x16 RAM, with your assignment(s)
  (on a machine with Quartus, run in DIR:  quartus_sh --flow compile probe   ~1-3 minutes)
  qsf_probe.py check DIR
      reads the reports/log: edition + version, every warning saying an assignment was ignored/unsupported/invalid,
      and the Fitter Settings rows whose value differs from the default (= options that actually took effect)

Verdicts to record in the knowledge base: ACCEPTED+APPLIED (setting shown as non-default), ACCEPTED-NOT-SHOWN (no error, no change
visible: inconclusive), REJECTED (warning/error text). Quote the exact lines as evidence and state edition and version.
"""
import argparse, glob, os, re, sys

V = """module probe(input clk, input [31:0] a, b, output reg [31:0] y, output reg [15:0] q);
  reg [31:0] r1, r2, r3;
  reg [15:0] mem [0:511];
  reg [8:0] ad = 0;
  always @(posedge clk) begin
    r1 <= a + b; r2 <= r1 + a; r3 <= r2 + b; y <= r3 + r1;
    ad <= ad + 1; mem[ad] <= y[15:0]; q <= mem[ad + 9'd7];
  end
endmodule
"""


def make(a):
    os.makedirs(a.dir, exist_ok=True)
    open(os.path.join(a.dir, "probe.v"), "w").write(V)
    open(os.path.join(a.dir, "probe.sdc"), "w").write("create_clock -name clk -period 10.0 [get_ports clk]\n")
    q = ['set_global_assignment -name FAMILY "Cyclone V"', "set_global_assignment -name DEVICE 5CEBA4F23C8",
         "set_global_assignment -name TOP_LEVEL_ENTITY probe", "set_global_assignment -name VERILOG_FILE probe.v",
         "set_global_assignment -name SDC_FILE probe.sdc", "set_global_assignment -name SEED 1"] + (a.assign or [])
    open(os.path.join(a.dir, "probe.qsf"), "w").write("\n".join(q) + "\n")
    open(os.path.join(a.dir, "probe.qpf"), "w").write('PROJECT_REVISION = "probe"\n')
    print(f"wrote {a.dir}. Run there: quartus_sh --flow compile probe   then: qsf_probe.py check {a.dir}")


def check(a):
    files = glob.glob(os.path.join(a.dir, "**", "*.rpt"), recursive=True) + glob.glob(os.path.join(a.dir, "**", "*.log"), recursive=True) \
        + glob.glob(os.path.join(a.dir, "**", "*.summary"), recursive=True) + glob.glob(os.path.join(a.dir, "**", "*.txt"), recursive=True)
    if not files:
        sys.exit("no reports found: compile first (quartus_sh --flow compile probe)")
    bad = re.compile(r"(ignor|not supported|unsupported|not available|invalid|unrecogni[sz]ed|unknown assignment|illegal value|cannot be used)", re.I)
    ver = None
    hits, applied = [], []
    for f in files:
        for line in open(f, encoding="utf-8", errors="ignore"):
            m = re.search(r"Quartus Prime Version\s*;?\s*([^;\n]+)", line)
            if m and not ver:
                ver = m.group(1).strip()
            if re.match(r"\s*(Warning|Error|Critical Warning)", line) and bad.search(line):
                hits.append(line.strip()[:220])
            r = re.match(r";\s*([^;]{6,80}?)\s*;\s*([^;]+?)\s*;\s*([^;]+?)\s*;\s*$", line)
            if r and r.group(2) != r.group(3) and "Setting" not in r.group(2) and f.endswith("fit.rpt"):
                applied.append(f"{r.group(1)}: {r.group(2)} (default {r.group(3)})")
    print("version/edition:", ver or "not found")
    print(f"\nrejected/ignored warnings ({len(set(hits))}):")
    for h in sorted(set(hits))[:25]:
        print("  ", h)
    print(f"\nfitter settings that differ from default = took effect ({len(set(applied))}):")
    for x in sorted(set(applied))[:40]:
        print("  ", x)
    verdict = "REJECTED" if hits else ("ACCEPTED+APPLIED (check that YOUR option is in the list above)" if applied else "ACCEPTED-NOT-SHOWN (inconclusive)")
    print("\nverdict:", verdict)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="c", required=True)
    m = sp.add_parser("make"); m.add_argument("dir"); m.add_argument("--assign", action="append")
    c = sp.add_parser("check"); c.add_argument("dir")
    a = ap.parse_args()
    make(a) if a.c == "make" else check(a)


if __name__ == "__main__":
    main()
