"""Render an executive-ready Markdown report."""
from __future__ import annotations
from datetime import date
from .register import Register
from .model import rating


def usd(x: float) -> str:
    return f"${x:,.0f}"


def ascii_heatmap(reg: Register) -> str:
    grid = reg.heatmap()
    lines = ["Impact"]
    for i, row in enumerate(grid):
        cells = " ".join(f"{','.join(c) or '.':^9}" for c in row)
        lines.append(f"  {5 - i} | {cells}")
    lines.append("    +" + "-" * 50)
    lines.append("      " + " ".join(f"{n:^9}" for n in range(1, 6)) + "  Likelihood")
    return "\n".join(lines)


def executive_report(reg: Register) -> str:
    t = reg.totals()
    counts = reg.rating_counts()
    out = ["# Cyber Risk Executive Summary",
           f"_Generated {date.today().isoformat()} | {len(reg.risks)} risks | "
           f"risk appetite threshold: residual score {reg.appetite}_", ""]

    out += ["## 1. Headline numbers", "",
            f"- **Inherent annualised loss exposure:** {usd(t['inherent_ale'])}",
            f"- **Residual annualised loss exposure:** {usd(t['residual_ale'])}",
            f"- **Value delivered by current controls:** {t['risk_reduction_pct']:.0f}% reduction",
            "- **Residual rating mix:** " + ", ".join(f"{k}: {v}" for k, v in counts.items()), ""]

    out += ["## 2. Top risks (by residual score)", "",
            "| ID | Risk | Owner | Inherent | Residual | Rating | Residual ALE | Treatment |",
            "|---|---|---|---|---|---|---|---|"]
    for r in reg.top(5):
        out.append(f"| {r.id} | {r.title} | {r.owner} | {r.inherent} | {r.residual} | "
                   f"{rating(r.residual)} | {usd(r.residual_ale)} | {r.treatment} |")
    out.append("")

    out += ["## 3. Risk appetite breaches requiring decision", ""]
    breaches = reg.appetite_breaches()
    if breaches:
        for r in breaches:
            out.append(f"- **{r.id} {r.title}**: residual {r.residual} exceeds appetite "
                       f"{reg.appetite} while treatment is *{r.treatment}*. Owner: {r.owner}. "
                       f"Escalate for formal acceptance or funded mitigation.")
    else:
        out.append("- None. All residual risks are within appetite or under active mitigation.")
    out.append("")

    out += ["## 4. Exposure by NIST CSF 2.0 function", "",
            "| Function | Risks | Residual ALE |", "|---|---|---|"]
    for fn, rs in sorted(reg.by("csf_function").items(),
                         key=lambda kv: -sum(r.residual_ale for r in kv[1])):
        out.append(f"| {fn.title()} | {len(rs)} | {usd(sum(r.residual_ale for r in rs))} |")
    out.append("")

    out += ["## 5. Exposure by CISSP domain", "",
            "| Domain | Risks | Avg residual |", "|---|---|---|"]
    for dom, rs in sorted(reg.by("cissp_domain").items()):
        out.append(f"| {dom} | {len(rs)} | {sum(r.residual for r in rs) / len(rs):.1f} |")
    out.append("")

    od = reg.overdue()
    out += ["## 6. Governance hygiene", "",
            f"- Overdue risk reviews: **{len(od)}**"
            + (" (" + ", ".join(r.id for r in od) + ")" if od else ""), ""]
    out += ["## 7. Inherent risk heatmap", "", "```", ascii_heatmap(reg), "```", ""]
    return "\n".join(out)
