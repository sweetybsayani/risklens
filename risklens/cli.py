"""Command-line interface: python -m risklens <command> <register.json>"""
from __future__ import annotations
import argparse
import sys
from .register import Register
from .report import executive_report, ascii_heatmap


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="risklens", description="Security risk register toolkit")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, help_ in [("validate", "check register integrity"),
                        ("report", "generate executive Markdown report"),
                        ("heatmap", "print inherent risk heatmap")]:
        s = sub.add_parser(name, help=help_)
        s.add_argument("register")
        if name == "report":
            s.add_argument("-o", "--output", help="write to file instead of stdout")
    a = p.parse_args(argv)

    reg = Register.load(a.register)
    errs = reg.validate()
    if a.cmd == "validate":
        print("\n".join(errs) if errs else f"OK: {len(reg.risks)} risks valid")
        return 1 if errs else 0
    if errs:
        print("Register invalid:\n" + "\n".join(errs), file=sys.stderr)
        return 1
    if a.cmd == "heatmap":
        print(ascii_heatmap(reg))
    else:
        text = executive_report(reg)
        if a.output:
            with open(a.output, "w") as f:
                f.write(text)
            print(f"Wrote {a.output}")
        else:
            print(text)
    return 0
