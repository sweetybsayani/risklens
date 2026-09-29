# RiskLens

A zero-dependency Python toolkit that turns a security risk register into an **executive-ready report**, combining qualitative 5x5 scoring with quantitative analysis (SLE / ALE), mapped to **NIST CSF 2.0** and the **CISSP eight domains**.

Built to answer the question leadership actually asks: *"What are our biggest risks, what could they cost us per year, and which ones need a decision from me?"*

## Features
- **Inherent vs residual scoring**: `likelihood x impact`, reduced by control effectiveness
- **Quantitative loss modelling**: SLE = AV x EF, ALE = SLE x ARO, plus residual ALE
- **Risk appetite enforcement**: flags residual risk above threshold that is not being mitigated
- **Governance hygiene**: detects overdue risk reviews
- **Framework mapping**: exposure rolled up by NIST CSF 2.0 function and CISSP domain
- **Register validation**: schema and range checks, duplicate ID detection
- **5x5 heatmap** and Markdown executive summary output

## Usage
```bash
python -m risklens validate data/sample_register.json
python -m risklens report data/sample_register.json -o report.md
python -m risklens heatmap data/sample_register.json
python -m unittest discover -s tests -t .
```
See [`sample_report.md`](sample_report.md) for example output.

## Methodology
| Metric | Formula |
|---|---|
| Inherent score | Likelihood (1-5) x Impact (1-5) |
| Residual score | Inherent x (1 - control effectiveness) |
| Rating bands | Critical >= 15, High >= 10, Medium >= 5, Low < 5 |
| SLE | Asset value x Exposure factor |
| ALE | SLE x Annualised rate of occurrence |
| Appetite breach | Residual > appetite AND treatment != mitigate |

## Roadmap
- CSV/Excel import, PDF export
- Control library mapped to ISO 27001 Annex A / NIST 800-53
- Monte Carlo (FAIR-style) loss simulation
- Risk trend tracking over time
